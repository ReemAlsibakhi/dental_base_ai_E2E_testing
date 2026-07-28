import { test as setup, expect } from '@playwright/test';
import * as path from 'path';
import * as fs from 'fs';

/**
 * Auth Setup — runs once before all tests.
 *
 * Selectors confirmed via Playwright codegen on live app:
 *   Landing page URL: /login (redirects to Keycloak)
 *   Email field: getByRole('textbox', { name: 'Email or Username' })
 *   Password field: getByRole('textbox', { name: 'Password' })
 *   Submit button: getByRole('button', { name: 'Log In' })
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

  // Navigate directly to login page
  await page.goto('/login', { waitUntil: 'load', timeout: 60_000 });

  // Click "Get started" → redirects to Keycloak
  await page.getByRole('button', { name: 'Get started' }).click();

  // Fill Keycloak login form
  await expect(page.getByRole('textbox', { name: 'Email or Username' })).toBeVisible();
  await page.getByRole('textbox', { name: 'Email or Username' }).fill(process.env.ADMIN_EMAIL);
  await page.getByRole('textbox', { name: 'Password' }).fill(process.env.ADMIN_PASSWORD);
  await page.getByRole('button', { name: 'Log In' }).click();

  // Verify authenticated
  await expect(page).not.toHaveURL(/.*login/, { timeout: 30_000 });
  await expect(page.locator('nav, main').first()).toBeVisible();

  // Save complete browser state
  fs.mkdirSync(path.dirname(AUTH_FILE), { recursive: true });
  await page.context().storageState({ path: AUTH_FILE });
  console.log('✅ Auth state saved');
});
