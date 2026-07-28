import { test as setup, expect } from '@playwright/test';
import * as path from 'path';
import * as fs from 'fs';

/**
 * Auth Setup — runs once before all tests.
 *
 * Follows Playwright official auth pattern:
 * https://playwright.dev/docs/auth
 *
 * Key decisions:
 *  - waitUntil: 'load' — waits for JS to load before React renders
 *  - Web First Assertions (expect) — auto-retry, no manual waitForSelector
 *  - Skip if .auth/admin.json exists — Playwright injects via storageState
 *  - No hardcoded credentials — throws if .env missing
 */

const AUTH_FILE = path.join(__dirname, '../.auth/admin.json');

setup('authenticate as admin', async ({ page }) => {
  // Skip if session already saved
  if (fs.existsSync(AUTH_FILE)) {
    console.log('✅ Auth file exists — skipping login');
    return;
  }

  if (!process.env.ADMIN_EMAIL || !process.env.ADMIN_PASSWORD) {
    throw new Error('Missing ADMIN_EMAIL or ADMIN_PASSWORD in .env');
  }

  const email    = process.env.ADMIN_EMAIL;
  const password = process.env.ADMIN_PASSWORD;

  // 'load' waits for JS bundle — React needs this before rendering
  await page.goto('/', { waitUntil: 'load', timeout: 60_000 });

  // Handle landing page using Web First Assertion (auto-retry built-in)
  const getStarted = page.getByRole('button', { name: /get started/i });
  if (await getStarted.isVisible()) {
    await getStarted.click();
  }

  // Wait for login form using Web First Assertions
  await expect(page.getByLabel(/username|email/i)).toBeVisible();
  await expect(page.getByLabel(/password/i)).toBeVisible();

  // Fill login form
  await page.getByLabel(/username|email/i).fill(email);
  await page.getByLabel(/password/i).fill(password);
  await page.getByRole('button', { name: /sign in|log in/i })
    .or(page.locator('button[type="submit"]'))
    .first()
    .click();

  // Verify successful authentication
  await expect(page).not.toHaveURL(/.*login/);
  await expect(page.locator('nav, main').first()).toBeVisible();

  // Save complete browser state
  fs.mkdirSync(path.dirname(AUTH_FILE), { recursive: true });
  await page.context().storageState({ path: AUTH_FILE });
  console.log('✅ Auth state saved');
});
