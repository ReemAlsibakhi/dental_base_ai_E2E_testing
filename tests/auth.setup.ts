import { test as setup, expect, Page } from '@playwright/test';
import * as path from 'path';
import * as fs from 'fs';

/**
 * Auth Setup — authenticates once and saves session for all tests.
 *
 * Flow:
 *   1. Check if saved session is still valid → reuse (fast path)
 *   2. If not → login via /login page → save session
 */

const AUTH_FILE = path.join(__dirname, '../.auth/admin.json');

async function isSessionValid(page: Page): Promise<boolean> {
  if (!fs.existsSync(AUTH_FILE)) return false;
  try {
    const state = JSON.parse(fs.readFileSync(AUTH_FILE, 'utf-8'));
    if (!state?.cookies?.length) return false;
    await page.context().addCookies(state.cookies);
    await page.goto('/settings', { waitUntil: 'commit', timeout: 15_000 });
    return page.url().includes('/settings');
  } catch {
    return false;
  }
}

async function saveSession(page: Page): Promise<void> {
  fs.mkdirSync(path.dirname(AUTH_FILE), { recursive: true });
  await page.context().storageState({ path: AUTH_FILE });
}

setup('authenticate as admin', async ({ page }) => {
  const email    = process.env.ADMIN_EMAIL    ?? 'reem_user';
  const password = process.env.ADMIN_PASSWORD ?? 'FaRe12345!!';

  // Fast path: reuse existing valid session
  if (await isSessionValid(page)) {
    console.log('✅ Reusing existing session');
    return;
  }

  // Navigate to app — redirects to /login automatically
  await page.goto('/', { waitUntil: 'commit', timeout: 30_000 });

  // Wait for login form to render
  const emailInput   = page.getByLabel(/email|username/i).or(page.locator('input[type="email"], input[name="username"]')).first();
  const passwordInput = page.getByLabel(/password/i).or(page.locator('input[type="password"]')).first();
  const submitButton  = page.locator('button[type="submit"]');

  await emailInput.waitFor({ state: 'visible', timeout: 30_000 });

  // Fill and submit
  await emailInput.fill(email);
  await passwordInput.fill(password);
  await submitButton.click();

  // Verify login succeeded — must redirect away from /login
  await page.waitForURL(
    (url) => !url.pathname.includes('/login'),
    { timeout: 30_000 }
  );

  // Confirm we're in the authenticated app
  await expect(page.locator('nav, main')).toBeVisible();

  await saveSession(page);
  console.log('✅ Login successful — session saved');
});
