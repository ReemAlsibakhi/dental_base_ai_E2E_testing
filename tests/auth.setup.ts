import { test as setup, expect, Page } from '@playwright/test';
import * as path from 'path';
import * as fs from 'fs';

/**
 * Auth Setup — runs once before all tests.
 *
 * Strategy:
 *  1. If saved session exists → try it (fast path)
 *  2. If session still valid  → reuse
 *  3. If session expired      → fresh Keycloak SSO login → save
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

  // App redirects to Keycloak SSO on unauthenticated access
  await page.goto('/settings', { waitUntil: 'commit', timeout: 30_000 });
  await page.waitForURL(/keycloak|auth|login/, { timeout: 30_000 });
  await page.waitForLoadState('domcontentloaded');

  // Fill Keycloak form
  await page.locator('#username').fill(email);
  await page.locator('#password').fill(password);
  await page.locator('#kc-login').click();

  // Wait for redirect back to app
  await page.waitForURL(`${BASE_URL}/settings**`, { timeout: 30_000 });

  // Save session
  fs.mkdirSync(path.dirname(AUTH_FILE), { recursive: true });
  await page.context().storageState({ path: AUTH_FILE });
  console.log('✅ Auth state saved');
}

setup('authenticate as admin', async ({ page }) => {

  // Fast path: try reusing saved session
  if (hasSavedSession()) {
    const state = JSON.parse(fs.readFileSync(AUTH_FILE, 'utf-8'));
    await page.context().addCookies(state.cookies);

    // Use 'commit' — fires as soon as server responds, avoids networkidle timeout
    await page.goto('/settings', { waitUntil: 'commit', timeout: 30_000 });

    // Give React time to render and handle auth redirect if needed
    await page.waitForURL(/.*/, { timeout: 10_000 });

    if (page.url().includes('/settings')) {
      console.log('✅ Reusing existing auth session');
      return;
    }

    console.log('⚠️  Session expired — performing fresh login');
  }

  await login(page);
});
