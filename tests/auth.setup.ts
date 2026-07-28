import { test as setup, expect } from '@playwright/test';
import * as path from 'path';
import * as fs from 'fs';

/**
 * Auth Setup — Playwright official authentication pattern.
 * @see https://playwright.dev/docs/auth
 *
 * Selectors confirmed via Playwright codegen on live app:
 *   page.getByRole('button', { name: 'Get started' })
 *   page.getByRole('textbox', { name: 'Email or Username' })
 *   page.getByRole('textbox', { name: 'Password' })
 *   page.getByRole('button', { name: 'Log In' })
 *
 * Session lifecycle:
 *   - First run  → login → save .auth/admin.json
 *   - Next runs  → file exists → skip login (Playwright injects via storageState)
 *   - Expiry     → delete .auth/admin.json → re-run
 */

const AUTH_FILE = path.join(__dirname, '../.auth/admin.json');

setup('authenticate as admin', async ({ page }) => {
  if (!process.env.ADMIN_EMAIL || !process.env.ADMIN_PASSWORD) {
    throw new Error('Missing ADMIN_EMAIL or ADMIN_PASSWORD in .env');
  }

  // Skip if valid session already saved
  if (fs.existsSync(AUTH_FILE)) {
    console.log('✅ Auth file exists — skipping login');
    return;
  }

  // Step 1: Navigate to login page
  await page.goto('/login');

  // Step 2: Click "Get started" → redirects to Keycloak
  await page.getByRole('button', { name: 'Get started' }).click();

  // Step 3: Fill Keycloak login form
  await page.getByRole('textbox', { name: 'Email or Username' }).fill(process.env.ADMIN_EMAIL);
  await page.getByRole('textbox', { name: 'Password' }).fill(process.env.ADMIN_PASSWORD);
  await page.getByRole('button', { name: 'Log In' }).click();

  // Step 4: Verify authenticated
  await expect(page).not.toHaveURL(/login/);

  // Step 5: Save complete browser state (cookies + localStorage)
  fs.mkdirSync(path.dirname(AUTH_FILE), { recursive: true });
  await page.context().storageState({ path: AUTH_FILE });
  console.log('✅ Auth state saved');
});
