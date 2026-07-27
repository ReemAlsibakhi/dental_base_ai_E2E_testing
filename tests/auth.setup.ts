import { test as setup, expect } from '@playwright/test';
import * as path from 'path';
import * as fs from 'fs';

/**
 * Auth Setup — runs once before all tests.
 *
 * Strategy:
 *  1. Check if saved auth state exists and is still valid
 *  2. If valid → reuse it (fast path)
 *  3. If not → perform fresh Keycloak SSO login and save state
 *
 * Saved state location: .auth/admin.json
 * Playwright automatically injects this into every test via playwright.config.ts
 */

const AUTH_FILE = path.join(__dirname, '../.auth/admin.json');
const BASE_URL  = process.env.BASE_URL ?? 'https://dentalbase-dev-v2.vercel.app';

async function isAuthValid(page: import('@playwright/test').Page): Promise<boolean> {
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
  if (fs.existsSync(AUTH_FILE) && await isAuthValid(page)) {
    console.log('✅ Reusing existing auth session');
    return;
  }

  // Fresh login via Keycloak SSO
  await page.goto('/settings', { waitUntil: 'commit', timeout: 30_000 });

  // Wait for Keycloak redirect
  await page.waitForURL(/keycloak|auth|login/, { timeout: 30_000 });
  await page.waitForLoadState('domcontentloaded');

  // Fill Keycloak login form
  await page.locator('#username').fill(email);
  await page.locator('#password').fill(password);
  await page.locator('#kc-login').click();

  // Verify redirect back to app
  await page.waitForURL(`${BASE_URL}/settings**`, { timeout: 30_000 });
  await expect(page.locator('body')).toBeVisible();

  // Save session for all tests
  fs.mkdirSync(path.dirname(AUTH_FILE), { recursive: true });
  await page.context().storageState({ path: AUTH_FILE });
  console.log('✅ Auth state saved:', AUTH_FILE);
});
