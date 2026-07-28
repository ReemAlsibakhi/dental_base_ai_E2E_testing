import { test as setup, expect } from '@playwright/test';
import * as path from 'path';
import * as fs from 'fs';

/**
 * Auth Setup — runs once before all tests.
 *
 * Performs fresh login and saves the complete browser state
 * (cookies + localStorage) to .auth/admin.json.
 *
 * Playwright injects this state into every test automatically
 * via storageState in playwright.config.ts — no manual session
 * management needed in tests.
 */

const AUTH_FILE = path.join(__dirname, '../.auth/admin.json');

setup('authenticate as admin', async ({ page }) => {
  const email    = process.env.ADMIN_EMAIL    ?? 'reem_user';
  const password = process.env.ADMIN_PASSWORD ?? 'FaRe12345!!';

  // Navigate to app — redirects to /login automatically
  await page.goto('/', { waitUntil: 'commit', timeout: 30_000 });

  // Wait for login form to render
  await page.waitForSelector('input[type="password"]', { timeout: 30_000 });

  // Fill credentials
  const emailInput    = page.locator('input[name="username"], input[type="email"], #username').first();
  const passwordInput = page.locator('input[type="password"]').first();
  const submitButton  = page.locator('button[type="submit"]').first();

  await emailInput.fill(email);
  await passwordInput.fill(password);
  await submitButton.click();

  // Wait for redirect to authenticated area
  await page.waitForURL(
    (url) => !url.pathname.includes('/login'),
    { timeout: 30_000 }
  );

  // Verify we are in the app
  await expect(page.locator('nav, main, [class*="sidebar"]').first()).toBeVisible();

  // Save complete browser state — cookies + localStorage
  fs.mkdirSync(path.dirname(AUTH_FILE), { recursive: true });
  await page.context().storageState({ path: AUTH_FILE });
  console.log('✅ Auth state saved');
});
