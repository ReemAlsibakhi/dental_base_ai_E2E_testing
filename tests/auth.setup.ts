import { test as setup, Page } from '@playwright/test';
import * as path from 'path';
import * as fs from 'fs';

/**
 * Auth Setup — runs once before all tests.
 *
 * Strategy: navigate to app, wait for full render, then handle state.
 */

const AUTH_FILE = path.join(__dirname, '../.auth/admin.json');

async function saveState(page: Page): Promise<void> {
  fs.mkdirSync(path.dirname(AUTH_FILE), { recursive: true });
  await page.context().storageState({ path: AUTH_FILE });
  console.log('✅ Auth state saved');
}

setup('authenticate as admin', async ({ page }) => {
  const email    = process.env.ADMIN_EMAIL    ?? 'reem_user';
  const password = process.env.ADMIN_PASSWORD ?? 'FaRe12345!!';

  // Navigate and wait for React to fully render
  await page.goto('/', { waitUntil: 'commit', timeout: 30_000 });

  // Wait for any input or known app element to appear
  await page.waitForSelector(
    '#username, input[type="email"], input[type="password"], button:has-text("Get started"), nav',
    { timeout: 30_000 }
  );

  const url = page.url();

  // Case 1: Already authenticated
  if (url.includes('/settings') || url.includes('/overview') || url.includes('/calls') || url.includes('/patients')) {
    await saveState(page);
    console.log('✅ Already authenticated');
    return;
  }

  // Case 2: On login page (DentalBase or Keycloak)
  const usernameField = page.locator('#username, input[name="username"], input[type="email"]').first();
  const passwordField = page.locator('#password, input[name="password"], input[type="password"]').first();
  const submitBtn     = page.locator('#kc-login, button[type="submit"]').first();

  if (await usernameField.isVisible()) {
    await usernameField.fill(email);
    await passwordField.fill(password);
    await submitBtn.click();
    await page.waitForURL('**/{settings,overview,calls,patients}**', { timeout: 30_000 });
    await saveState(page);
    return;
  }

  // Case 3: Landing page
  const getStarted = page.getByText('Get started', { exact: true });
  if (await getStarted.isVisible()) {
    await getStarted.click();
    await page.waitForSelector('#username, input[type="email"]', { timeout: 30_000 });
    await page.locator('#username, input[type="email"]').first().fill(email);
    await page.locator('#password, input[type="password"]').first().fill(password);
    await page.locator('#kc-login, button[type="submit"]').first().click();
    await page.waitForURL('**/{settings,overview,calls,patients}**', { timeout: 30_000 });
    await saveState(page);
    return;
  }

  throw new Error(`Unknown page state: ${url}`);
});
