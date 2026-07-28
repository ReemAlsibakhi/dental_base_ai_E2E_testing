import { test as setup, expect } from '@playwright/test';
import * as path from 'path';
import * as fs from 'fs';

/**
 * Auth Setup — performs login once and saves session for all tests.
 *
 * App is hosted on Vercel — cold starts can take 30-60 seconds.
 * We wait for specific DOM elements instead of network state.
 */

const AUTH_FILE = path.join(__dirname, '../.auth/admin.json');

setup('authenticate as admin', async ({ page }) => {
  const email    = process.env.ADMIN_EMAIL    ?? 'reem_user';
  const password = process.env.ADMIN_PASSWORD ?? 'FaRe12345!!';

  await page.goto('/', { waitUntil: 'commit', timeout: 60_000 });

  // Wait for app to finish loading — Vercel cold start can be slow
  await page.waitForSelector('button, input[type="password"]', {
    state: 'visible',
    timeout: 60_000,
  });

  // If on landing page → click "Get started"
  const getStarted = page.locator('button').filter({ hasText: 'Get started' });
  if (await getStarted.isVisible()) {
    await getStarted.click();
    await page.waitForSelector('input[type="password"]', { timeout: 30_000 });
  }

  // Fill login credentials
  await page.locator('input[name="username"], #username').first().fill(email);
  await page.locator('input[type="password"]').first().fill(password);
  await page.locator('button[type="submit"]').first().click();

  // Wait for app to load after login
  await page.waitForFunction(
    () => !window.location.pathname.startsWith('/login'),
    { timeout: 30_000 }
  );

  await expect(page.locator('nav, main').first()).toBeVisible({ timeout: 15_000 });

  fs.mkdirSync(path.dirname(AUTH_FILE), { recursive: true });
  await page.context().storageState({ path: AUTH_FILE });
  console.log('✅ Auth state saved');
});
