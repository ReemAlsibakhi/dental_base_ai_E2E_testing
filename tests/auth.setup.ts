import { test as setup, Page } from '@playwright/test';
import * as path from 'path';
import * as fs from 'fs';

/**
 * Auth Setup — runs once before all tests.
 *
 * Navigates to the app and handles whatever page state we land on:
 *  - /settings     → already authenticated → save state
 *  - /login        → DentalBase login page → fill credentials → save state
 *  - Keycloak      → fill credentials → save state
 *  - Landing page  → click Get started → fill credentials → save state
 */

const AUTH_FILE = path.join(__dirname, '../.auth/admin.json');

async function fillAndSubmit(page: Page, email: string, password: string): Promise<void> {
  // Try DentalBase login form first, then Keycloak
  const usernameField = page.locator('#username, input[name="username"], input[type="email"]').first();
  const passwordField = page.locator('#password, input[name="password"], input[type="password"]').first();
  const submitBtn     = page.locator('#kc-login, button[type="submit"]').first();

  await usernameField.fill(email);
  await passwordField.fill(password);
  await submitBtn.click();
  await page.waitForURL('**/settings**', { timeout: 30_000 });
}

async function saveState(page: Page): Promise<void> {
  fs.mkdirSync(path.dirname(AUTH_FILE), { recursive: true });
  await page.context().storageState({ path: AUTH_FILE });
  console.log('✅ Auth state saved');
}

setup('authenticate as admin', async ({ page }) => {
  const email    = process.env.ADMIN_EMAIL    ?? 'reem_user';
  const password = process.env.ADMIN_PASSWORD ?? 'FaRe12345!!';

  await page.goto('/', { waitUntil: 'domcontentloaded', timeout: 30_000 });
  await page.waitForTimeout(2000);

  const url = page.url();

  // Already authenticated
  if (url.includes('/settings') || url.includes('/overview') || url.includes('/calls')) {
    await page.goto('/settings', { waitUntil: 'domcontentloaded', timeout: 30_000 });
    await saveState(page);
    console.log('✅ Already authenticated');
    return;
  }

  // DentalBase /login page or Keycloak
  if (url.includes('/login') || await page.locator('#username, input[type="email"]').first().isVisible()) {
    // Wait for React to render the login form
    const usernameField = page.locator('#username, input[name="username"], input[type="email"]').first();
    await usernameField.waitFor({ state: 'visible', timeout: 30_000 });
    await fillAndSubmit(page, email, password);
    await saveState(page);
    return;
  }

  // Landing page with "Get started"
  const getStarted = page.getByText('Get started', { exact: true });
  if (await getStarted.isVisible()) {
    await getStarted.click();
    await page.waitForTimeout(2000);
    await fillAndSubmit(page, email, password);
    await saveState(page);
    return;
  }

  throw new Error(`Unknown page state: ${url} — please check the app manually`);
});
