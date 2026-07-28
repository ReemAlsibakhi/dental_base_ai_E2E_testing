import { test as setup, expect, Page } from '@playwright/test';
import * as path from 'path';
import * as fs from 'fs';

/**
 * Auth Setup — authenticates once, validates session on every run.
 *
 * Why validate instead of just checking file existence?
 * Cookies/tokens expire — a stale .auth/admin.json causes silent failures.
 * We navigate to a protected page to confirm the session is truly valid.
 */

const AUTH_FILE = path.join(__dirname, '../.auth/admin.json');

if (!process.env.ADMIN_EMAIL || !process.env.ADMIN_PASSWORD) {
  throw new Error('Missing required env vars: ADMIN_EMAIL and ADMIN_PASSWORD');
}

async function isSessionValid(page: Page): Promise<boolean> {
  if (!fs.existsSync(AUTH_FILE)) return false;
  try {
    const state = JSON.parse(fs.readFileSync(AUTH_FILE, 'utf-8'));
    if (!state?.cookies?.length) return false;

    await page.context().addCookies(state.cookies);
    await page.goto('/settings', { waitUntil: 'commit', timeout: 15_000 });

    // Confirm we are on settings — not redirected to /login
    await expect(page).not.toHaveURL(/.*login/, { timeout: 10_000 });
    return true;
  } catch {
    return false;
  }
}

setup('authenticate as admin', async ({ page }) => {
  const email    = process.env.ADMIN_EMAIL!;
  const password = process.env.ADMIN_PASSWORD!;

  // Validate existing session — reuse if still valid
  if (await isSessionValid(page)) {
    console.log('✅ Existing session is valid — skipping login');
    return;
  }

  // Navigate to app — React SPA redirects to /login
  await page.goto('/', { waitUntil: 'commit', timeout: 30_000 });

  // Wait for React to render the UI
  await page.waitForSelector('button, input[type="password"]', {
    state: 'visible',
    timeout: 60_000,
  });

  // Handle landing page
  const getStarted = page.getByRole('button', { name: /get started/i });
  if (await getStarted.isVisible()) {
    await getStarted.click();
    await page.waitForSelector('input[type="password"]', {
      state: 'visible',
      timeout: 30_000,
    });
  }

  // Fill login form using user-facing locators
  await page.getByLabel(/username|email/i).fill(email);
  await page.getByLabel(/password/i).fill(password);
  await page.getByRole('button', { name: /sign in|log in|submit/i })
            .or(page.locator('button[type="submit"]'))
            .first()
            .click();

  // Wait for redirect away from /login
  await expect(page).not.toHaveURL(/.*login/, { timeout: 30_000 });
  await expect(page.locator('nav, main').first()).toBeVisible();

  // Save complete browser state (cookies + localStorage)
  fs.mkdirSync(path.dirname(AUTH_FILE), { recursive: true });
  await page.context().storageState({ path: AUTH_FILE });
  console.log('✅ Auth state saved');
});
