import { test as setup, expect } from '@playwright/test';
import * as path from 'path';
import * as fs from 'fs';

/**
 * Auth Setup — runs once before all tests.
 *
 * Follows Playwright's official authentication pattern:
 * https://playwright.dev/docs/auth
 *
 * - If .auth/admin.json exists → skip (Playwright injects it via storageState)
 * - If not → login → save storageState
 * - If session expires → delete .auth/admin.json and re-run
 *
 * Credentials must be set in .env — never hardcoded.
 */

const AUTH_FILE = path.join(__dirname, '../.auth/admin.json');

setup('authenticate as admin', async ({ page }) => {
  // Skip if session already saved
  if (fs.existsSync(AUTH_FILE)) {
    console.log('✅ Auth file exists — skipping login');
    return;
  }

  if (!process.env.ADMIN_EMAIL || !process.env.ADMIN_PASSWORD) {
    throw new Error(
      'Missing ADMIN_EMAIL or ADMIN_PASSWORD in .env'
    );
  }

  const email    = process.env.ADMIN_EMAIL;
  const password = process.env.ADMIN_PASSWORD;

  // Navigate — React SPA, commit fires before render
  await page.goto('/', { waitUntil: 'commit', timeout: 30_000 });

  // Wait for React to render any interactive element
  await page.waitForSelector('button, input[type="password"]', {
    state: 'visible',
    timeout: 60_000,
  });

  // Handle landing page "Get started"
  const getStarted = page.getByRole('button', { name: /get started/i });
  if (await getStarted.isVisible()) {
    await getStarted.click();
    await page.waitForSelector('input[type="password"]', {
      state: 'visible',
      timeout: 30_000,
    });
  }

  // Fill login form
  await page.getByLabel(/username|email/i).fill(email);
  await page.getByLabel(/password/i).fill(password);
  await page.getByRole('button', { name: /sign in|log in/i })
    .or(page.locator('button[type="submit"]'))
    .first()
    .click();

  // Verify successful authentication
  await expect(page).not.toHaveURL(/.*login/, { timeout: 30_000 });
  await expect(page.locator('nav, main').first()).toBeVisible();

  // Save complete browser state
  fs.mkdirSync(path.dirname(AUTH_FILE), { recursive: true });
  await page.context().storageState({ path: AUTH_FILE });
  console.log('✅ Auth state saved');
});
