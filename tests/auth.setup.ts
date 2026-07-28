import { test as setup, expect } from '@playwright/test';
import * as path from 'path';
import * as fs from 'fs';

/**
 * Auth Setup — performs login and saves complete browser state.
 *
 * App flow:
 *   / → landing page ("Welcome back" + "Get started")
 *     → click "Get started"
 *     → /login (username + password form)
 *     → fill credentials → submit
 *     → authenticated app
 */

const AUTH_FILE = path.join(__dirname, '../.auth/admin.json');

setup('authenticate as admin', async ({ page }) => {
  const email    = process.env.ADMIN_EMAIL    ?? 'reem_user';
  const password = process.env.ADMIN_PASSWORD ?? 'FaRe12345!!';

  // Step 1: Navigate to app
  await page.goto('/', { waitUntil: 'commit', timeout: 30_000 });

  // Step 2: Click "Get started" on landing page
  const getStarted = page.getByText('Get started');
  await getStarted.waitFor({ state: 'visible', timeout: 30_000 });
  await getStarted.click();

  // Step 3: Wait for login form
  await page.waitForSelector('input[type="password"]', { timeout: 30_000 });

  // Step 4: Fill credentials
  await page.locator('input[name="username"], input[type="email"], #username').first().fill(email);
  await page.locator('input[type="password"]').first().fill(password);
  await page.locator('button[type="submit"]').first().click();

  // Step 5: Wait for authenticated redirect
  await page.waitForURL(
    (url) => !url.pathname.includes('/login'),
    { timeout: 30_000 }
  );

  await expect(page.locator('nav, main').first()).toBeVisible();

  // Step 6: Save complete state
  fs.mkdirSync(path.dirname(AUTH_FILE), { recursive: true });
  await page.context().storageState({ path: AUTH_FILE });
  console.log('✅ Auth state saved');
});
