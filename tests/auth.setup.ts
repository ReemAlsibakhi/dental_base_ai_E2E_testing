import { test as setup } from '@playwright/test';
import * as path from 'path';
import * as fs from 'fs';

const AUTH_FILE = path.join(__dirname, '../.auth/admin.json');
const PYTHON_AUTH_FILE = path.join(__dirname, '../.playwright_auth/admin.json');

setup('authenticate as admin', async ({ page }) => {
  const email    = process.env.ADMIN_EMAIL    ?? 'reem_user';
  const password = process.env.ADMIN_PASSWORD ?? 'FaRe12345!!';

  // Reuse Python auth state if available and valid
  for (const src of [AUTH_FILE, PYTHON_AUTH_FILE]) {
    if (fs.existsSync(src)) {
      const state = JSON.parse(fs.readFileSync(src, 'utf-8'));
      if (state?.cookies?.length > 0) {
        await page.context().addCookies(state.cookies);
        await page.goto('/settings', { waitUntil: 'commit', timeout: 30_000 });
        await page.waitForTimeout(4_000);
        if (page.url().includes('/settings')) {
          fs.mkdirSync(path.dirname(AUTH_FILE), { recursive: true });
          await page.context().storageState({ path: AUTH_FILE });
          console.log('✅ Auth state reused from:', src);
          return;
        }
      }
    }
  }

  // Fresh login via Keycloak SSO
  await page.goto('/settings', { waitUntil: 'commit', timeout: 30_000 });
  await page.waitForTimeout(4_000);

  // Wait for Keycloak redirect
  try {
    await page.waitForURL(/keycloak|auth|login|accounts/, { timeout: 15_000 });
  } catch {
    // Maybe already on login page without redirect
  }

  await page.waitForLoadState('domcontentloaded');

  // Keycloak form
  const usernameField = page.locator('#username').or(page.locator('input[name="username"]'));
  const passwordField = page.locator('#password').or(page.locator('input[name="password"]'));
  const submitBtn     = page.locator('#kc-login').or(page.locator('button[type="submit"]'));

  await usernameField.waitFor({ state: 'visible', timeout: 15_000 });
  await usernameField.fill(email);
  await passwordField.fill(password);
  await submitBtn.click();

  await page.waitForURL('**/settings**', { timeout: 30_000 });

  fs.mkdirSync(path.dirname(AUTH_FILE), { recursive: true });
  await page.context().storageState({ path: AUTH_FILE });
  console.log('✅ Auth state saved');
});
