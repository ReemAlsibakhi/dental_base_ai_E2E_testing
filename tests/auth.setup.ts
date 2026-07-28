import { test as setup, expect } from '@playwright/test';
import * as path from 'path';
import * as fs from 'fs';

/**
 * Auth Setup — performs login once and saves session for all tests.
 *
 * App flow:
 *   / → loading screen → landing page ("Get started") → /login → authenticated app
 */

const AUTH_FILE = path.join(__dirname, '../.auth/admin.json');

setup('authenticate as admin', async ({ page }) => {
  const email    = process.env.ADMIN_EMAIL    ?? 'reem_user';
  const password = process.env.ADMIN_PASSWORD ?? 'FaRe12345!!';

  await page.goto('/', { waitUntil: 'networkidle', timeout: 60_000 });

  // Wait for either landing page button or login form
  await page.waitForSelector(
    'button, input[type="password"], input[name="username"]',
    { timeout: 30_000 }
  );

  // If landing page → click Get started
  const btn = page.locator('button').first();
  const btnText = await btn.textContent();
  if (btnText?.trim() === 'Get started') {
    await btn.click();
    await page.waitForSelector('input[type="password"]', { timeout: 30_000 });
  }

  // Fill credentials
  await page.locator('input[name="username"], input[type="email"], #username').first().fill(email);
  await page.locator('input[type="password"]').first().fill(password);
  await page.locator('button[type="submit"]').first().click();

  // Wait for authenticated redirect — URL changes from /login to app page
  await page.waitForFunction(
    () => !window.location.pathname.startsWith('/login'),
    { timeout: 30_000 }
  );

  await expect(page.locator('nav, main').first()).toBeVisible();

  // Save complete browser state
  fs.mkdirSync(path.dirname(AUTH_FILE), { recursive: true });
  await page.context().storageState({ path: AUTH_FILE });
  console.log('✅ Auth state saved');
});
