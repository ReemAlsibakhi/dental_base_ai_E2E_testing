import { test as setup } from '@playwright/test';
import * as path from 'path';
import * as fs from 'fs';

/**
 * Auth Setup — reuses Python save_session.py state if available,
 * otherwise performs fresh Keycloak login.
 */

const AUTH_FILE = path.join(__dirname, '../.auth/admin.json');

// Python Playwright saves auth here
const PYTHON_AUTH_FILE = path.join(__dirname, '../.playwright_auth/admin.json');

setup('authenticate as admin', async ({ page }) => {
  // Option 1: Reuse Python auth state (from save_session.py)
  if (fs.existsSync(PYTHON_AUTH_FILE)) {
    const state = JSON.parse(fs.readFileSync(PYTHON_AUTH_FILE, 'utf-8'));
    if (state?.cookies?.length > 0) {
      fs.mkdirSync(path.dirname(AUTH_FILE), { recursive: true });
      fs.copyFileSync(PYTHON_AUTH_FILE, AUTH_FILE);

      // Verify session is still valid
      await page.context().addCookies(state.cookies);
      await page.goto('/settings', { waitUntil: 'commit', timeout: 30_000 });
      await page.waitForTimeout(3000);

      if (page.url().includes('/settings')) {
        console.log('✅ Reusing Python auth state');
        return;
      }
      console.log('⚠️  Python auth expired, doing fresh login...');
    }
  }

  // Option 2: Fresh Keycloak login
  const email    = process.env.ADMIN_EMAIL    ?? 'reem_user';
  const password = process.env.ADMIN_PASSWORD ?? 'FaRe12345!!';

  await page.goto('/settings', { waitUntil: 'commit', timeout: 30_000 });

  // Wait for app to load and redirect to Keycloak
  await page.waitForTimeout(3000);
  await page.waitForURL(/keycloak|auth|login|accounts/, { timeout: 30_000 });
  await page.waitForLoadState('domcontentloaded');

  // Fill Keycloak form
  await page.locator('#username').or(page.locator('input[name="username"]')).fill(email);
  await page.locator('#password').or(page.locator('input[name="password"]')).fill(password);
  await page.locator('#kc-login').or(page.locator('button[type="submit"]')).click();

  // Wait for app
  await page.waitForURL('**/settings**', { timeout: 30_000 });

  // Save state
  fs.mkdirSync(path.dirname(AUTH_FILE), { recursive: true });
  await page.context().storageState({ path: AUTH_FILE });
  console.log('✅ Auth state saved');
});
