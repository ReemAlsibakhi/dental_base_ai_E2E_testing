import { test as setup } from '@playwright/test';
import * as path from 'path';
import * as fs from 'fs';

const AUTH_FILE = path.join(__dirname, '../.auth/admin.json');

setup('authenticate as admin', async ({ page }) => {
  const email = process.env.ADMIN_EMAIL ?? 'reem_user';
  const password = process.env.ADMIN_PASSWORD ?? 'FaRe12345!!';
  const baseURL = process.env.BASE_URL ?? 'https://dentalbase-dev-v2.vercel.app';

  // Reuse existing auth if valid
  if (fs.existsSync(AUTH_FILE)) {
    const state = JSON.parse(fs.readFileSync(AUTH_FILE, 'utf-8'));
    if (state?.cookies?.length > 0) {
      await page.context().addCookies(state.cookies);
      await page.goto(`${baseURL}/settings`, { waitUntil: 'networkidle', timeout: 30_000 });
      if (page.url().includes('/settings')) {
        console.log('Reusing existing auth state');
        return;
      }
    }
  }

  // Navigate to app — will redirect to Keycloak
  await page.goto(`${baseURL}/settings`, { waitUntil: 'commit', timeout: 30_000 });

  // Wait for Keycloak login page to load
  await page.waitForURL(/keycloak|auth|login/, { timeout: 30_000 });
  await page.waitForLoadState('domcontentloaded', { timeout: 30_000 });

  // Keycloak login form
  await page.fill('#username, input[name="username"]', email);
  await page.fill('#password, input[name="password"]', password);
  await page.click('#kc-login, button[type="submit"]');

  // Wait for redirect back to app
  await page.waitForURL(`${baseURL}/**`, { timeout: 30_000 });

  // Save auth state
  fs.mkdirSync(path.dirname(AUTH_FILE), { recursive: true });
  await page.context().storageState({ path: AUTH_FILE });
  console.log('Auth state saved to', AUTH_FILE);
});
