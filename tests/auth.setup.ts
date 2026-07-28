import { test as setup, Page } from '@playwright/test';
import * as path from 'path';
import * as fs from 'fs';

/**
 * Auth Setup — runs once before all tests.
 *
 * Strategy:
 *  1. Navigate to /settings
 *  2. If already authenticated → save state and done
 *  3. If on landing page → click "Get started" → Keycloak login → save state
 *  4. If on Keycloak → login directly → save state
 */

const AUTH_FILE = path.join(__dirname, '../.auth/admin.json');

setup('authenticate as admin', async ({ page }) => {
  const email    = process.env.ADMIN_EMAIL    ?? 'reem_user';
  const password = process.env.ADMIN_PASSWORD ?? 'FaRe12345!!';

  await page.goto('/settings', { waitUntil: 'domcontentloaded', timeout: 30_000 });
  await page.waitForTimeout(3000);

  const url = page.url();

  // Case 1: Already on settings — save and done
  if (url.includes('/settings')) {
    fs.mkdirSync(path.dirname(AUTH_FILE), { recursive: true });
    await page.context().storageState({ path: AUTH_FILE });
    console.log('✅ Already authenticated — state saved');
    return;
  }

  // Case 2: On Keycloak login page
  if (await page.locator('#username').isVisible()) {
    await page.locator('#username').fill(email);
    await page.locator('#password').fill(password);
    await page.locator('#kc-login').click();
    await page.waitForURL('**/settings**', { timeout: 30_000 });
    fs.mkdirSync(path.dirname(AUTH_FILE), { recursive: true });
    await page.context().storageState({ path: AUTH_FILE });
    console.log('✅ Logged in via Keycloak — state saved');
    return;
  }

  // Case 3: On landing page — click "Get started" → triggers Keycloak redirect
  const getStarted = page.getByText('Get started', { exact: true });
  if (await getStarted.isVisible()) {
    await getStarted.click();
    await page.waitForSelector('#username', { timeout: 30_000 });
    await page.locator('#username').fill(email);
    await page.locator('#password').fill(password);
    await page.locator('#kc-login').click();
    await page.waitForURL('**/settings**', { timeout: 30_000 });
    fs.mkdirSync(path.dirname(AUTH_FILE), { recursive: true });
    await page.context().storageState({ path: AUTH_FILE });
    console.log('✅ Logged in via landing page — state saved');
    return;
  }

  throw new Error(`Unexpected page state: ${url}`);
});
