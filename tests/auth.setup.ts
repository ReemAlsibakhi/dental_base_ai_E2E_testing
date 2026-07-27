import { test as setup, expect, Page } from '@playwright/test';
import * as path from 'path';
import * as fs from 'fs';

/**
 * Auth Setup — runs once before all tests.
 *
 * Strategy:
 *  1. Check if saved auth file exists and has cookies
 *  2. Try to navigate with saved cookies — if /settings loads → valid
 *  3. If invalid or no file → fresh Keycloak SSO login → save state
 */

const AUTH_FILE = path.join(__dirname, '../.auth/admin.json');
const BASE_URL  = process.env.BASE_URL ?? 'https://dentalbase-dev-v2.vercel.app';

function hasSavedSession(): boolean {
  try {
    const state = JSON.parse(fs.readFileSync(AUTH_FILE, 'utf-8'));
    return Array.isArray(state?.cookies) && state.cookies.length > 0;
  } catch {
    return false;
  }
}

async function login(page: Page): Promise<void> {
  const email    = process.env.ADMIN_EMAIL    ?? 'reem_user';
  const password = process.env.ADMIN_PASSWORD ?? 'FaRe12345!!';

  await page.goto('/settings', { waitUntil: 'commit', timeout: 30_000 });
  await page.waitForURL(/keycloak|auth|login/, { timeout: 30_000 });
  await page.waitForLoadState('domcontentloaded');

  await page.locator('#username').fill(email);
  await page.locator('#password').fill(password);
  await page.locator('#kc-login').click();

  await page.waitForURL(`${BASE_URL}/settings**`, { timeout: 30_000 });
  await expect(page.locator('h1, h2, nav').first()).toBeVisible();

  fs.mkdirSync(path.dirname(AUTH_FILE), { recursive: true });
  await page.context().storageState({ path: AUTH_FILE });
  console.log('✅ Auth state saved');
}

setup('authenticate as admin', async ({ page }) => {
  // Fast path: try existing session first
  if (hasSavedSession()) {
    const state = JSON.parse(fs.readFileSync(AUTH_FILE, 'utf-8'));
    await page.context().addCookies(state.cookies);
    await page.goto('/settings', { waitUntil: 'networkidle', timeout: 30_000 });

    if (page.url().includes('/settings')) {
      console.log('✅ Reusing existing auth session');
      return;
    }
  }

  // Fresh login
  await login(page);
});
