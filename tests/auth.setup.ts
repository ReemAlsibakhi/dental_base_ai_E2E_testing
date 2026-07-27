import { test as setup, expect, Page } from '@playwright/test';
import * as path from 'path';
import * as fs from 'fs';

/**
 * Auth Setup — runs once before all tests.
 *
 * Strategy:
 *  1. If saved auth exists → verify it's still valid against live app
 *  2. If valid  → reuse (fast path, no login needed)
 *  3. If invalid → clear stale cookies → fresh Keycloak SSO login → save
 *
 * Saved state: .auth/admin.json
 * Injected into every test via storageState in playwright.config.ts
 */

const AUTH_FILE = path.join(__dirname, '../.auth/admin.json');
const BASE_URL  = process.env.BASE_URL ?? 'https://dentalbase-dev-v2.vercel.app';

async function isSessionValid(page: Page): Promise<boolean> {
  try {
    const state = JSON.parse(fs.readFileSync(AUTH_FILE, 'utf-8'));
    if (!state?.cookies?.length) return false;

    await page.context().addCookies(state.cookies);
    await page.goto('/settings', { waitUntil: 'networkidle', timeout: 30_000 });

    return page.url().includes('/settings');
  } catch {
    return false;
  }
}

setup('authenticate as admin', async ({ page }) => {
  const email    = process.env.ADMIN_EMAIL    ?? 'reem_user';
  const password = process.env.ADMIN_PASSWORD ?? 'FaRe12345!!';

  // Fast path: reuse existing valid session
  if (fs.existsSync(AUTH_FILE) && await isSessionValid(page)) {
    console.log('✅ Reusing existing auth session');
    return;
  }

  // Clear any stale cookies before fresh login
  await page.context().clearCookies();

  // Navigate to app — triggers Keycloak SSO redirect
  await page.goto('/settings', { waitUntil: 'commit', timeout: 30_000 });
  await page.waitForURL(/keycloak|auth|login/, { timeout: 30_000 });
  await page.waitForLoadState('domcontentloaded');

  // Fill Keycloak login form
  await page.locator('#username').fill(email);
  await page.locator('#password').fill(password);
  await page.locator('#kc-login').click();

  // Verify successful redirect back to app
  await page.waitForURL(`${BASE_URL}/settings**`, { timeout: 30_000 });
  await expect(page.getByText('Settings', { exact: false }).first()).toBeVisible();

  // Persist session for all tests
  fs.mkdirSync(path.dirname(AUTH_FILE), { recursive: true });
  await page.context().storageState({ path: AUTH_FILE });
  console.log('✅ Auth state saved:', AUTH_FILE);
});
