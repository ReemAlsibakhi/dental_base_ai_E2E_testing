import { chromium, FullConfig } from '@playwright/test';
import * as path from 'path';
import * as fs from 'fs';

/**
 * Global Setup — runs before everything else.
 *
 * Validates existing session on every run.
 * If expired → deletes .auth/admin.json so auth.setup.ts re-runs login.
 * This prevents tests from reaching /login instead of the app.
 *
 * @see https://playwright.dev/docs/test-global-setup-teardown
 */

const AUTH_FILE = path.join(__dirname, '.auth/admin.json');

async function globalSetup(config: FullConfig) {
  if (!fs.existsSync(AUTH_FILE)) {
    console.log('ℹ️  No auth file — auth.setup.ts will handle login');
    return;
  }

  const browser = await chromium.launch();
  const context = await browser.newContext({ storageState: AUTH_FILE });
  const page    = await context.newPage();

  const baseURL = process.env.BASE_URL ?? 'https://dentalbase-dev-v2.vercel.app';

  try {
    await page.goto(`${baseURL}/settings`, { waitUntil: 'commit', timeout: 15_000 });
    await page.waitForTimeout(3_000);
    const isValid = page.url().includes('/settings');

    if (isValid) {
      console.log('✅ Session valid — skipping login');
    } else {
      fs.unlinkSync(AUTH_FILE);
      console.log('⚠️  Session expired — deleted auth file, login will run');
    }
  } catch {
    fs.unlinkSync(AUTH_FILE);
    console.log('⚠️  Session check failed — deleted auth file, login will run');
  } finally {
    await browser.close();
  }
}

export default globalSetup;
