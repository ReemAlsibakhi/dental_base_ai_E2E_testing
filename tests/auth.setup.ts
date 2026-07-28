import { test as setup, expect } from '@playwright/test';
import * as path from 'path';
import * as fs from 'fs';

/**
 * Auth Setup — login once, reuse session for all subsequent runs.
 *
 * First run:  login → save .auth/admin.json
 * Next runs:  skip login — storageState in config handles injection
 */

const AUTH_FILE = path.join(__dirname, '../.auth/admin.json');

setup('authenticate as admin', async ({ page }) => {
  const email    = process.env.ADMIN_EMAIL    ?? 'reem_user';
  const password = process.env.ADMIN_PASSWORD ?? 'FaRe12345!!';

  // Skip login if session already saved
  if (fs.existsSync(AUTH_FILE)) {
    console.log('✅ Auth file exists — skipping login');
    return;
  }

  // Navigate to app
  await page.goto('/', { waitUntil: 'commit', timeout: 60_000 });

  // Wait for app to render
  await page.waitForSelector('button, input[type="password"]', {
    state: 'visible',
    timeout: 60_000,
  });

  // Click "Get started" if on landing page
  const getStarted = page.locator('button').filter({ hasText: 'Get started' });
  if (await getStarted.isVisible()) {
    await getStarted.click();
    await page.waitForSelector('input[type="password"]', { timeout: 30_000 });
  }

  // Fill credentials and submit
  await page.locator('input[name="username"], #username').first().fill(email);
  await page.locator('input[type="password"]').first().fill(password);
  await page.locator('button[type="submit"]').first().click();

  // Wait for authenticated app
  await page.waitForFunction(
    () => !window.location.pathname.startsWith('/login'),
    { timeout: 30_000 }
  );
  await expect(page.locator('nav, main').first()).toBeVisible({ timeout: 15_000 });

  // Save session
  fs.mkdirSync(path.dirname(AUTH_FILE), { recursive: true });
  await page.context().storageState({ path: AUTH_FILE });
  console.log('✅ Auth state saved');
});
