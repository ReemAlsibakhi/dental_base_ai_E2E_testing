import { test as setup, expect } from '@playwright/test';
import * as path from 'path';
import * as fs from 'fs';

/**
 * Auth Setup — performs login once and saves session for all tests.
 *
 * App flow:
 *   / → React SPA loads → landing page → "Get started" → /login → app
 *
 * Key insight: never use networkidle on SPAs with polling.
 * Instead, wait for specific elements to appear.
 */

const AUTH_FILE = path.join(__dirname, '../.auth/admin.json');

setup('authenticate as admin', async ({ page }) => {
  const email    = process.env.ADMIN_EMAIL    ?? 'reem_user';
  const password = process.env.ADMIN_PASSWORD ?? 'FaRe12345!!';

  // Navigate — commit fires when server responds, before React renders
  await page.goto('/', { waitUntil: 'commit', timeout: 30_000 });

  // Wait for React to render — watch for landing page button or login form
  await page.waitForSelector('button, input[type="password"]', { timeout: 30_000 });

  // If on landing page → click "Get started"
  if (await page.locator('button').filter({ hasText: 'Get started' }).isVisible()) {
    await page.locator('button').filter({ hasText: 'Get started' }).click();
    // Wait for login form to appear
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

  // Verify we are authenticated
  await expect(page.locator('nav, main').first()).toBeVisible({ timeout: 15_000 });

  // Save complete browser state (cookies + localStorage)
  fs.mkdirSync(path.dirname(AUTH_FILE), { recursive: true });
  await page.context().storageState({ path: AUTH_FILE });
  console.log('✅ Auth state saved');
});
