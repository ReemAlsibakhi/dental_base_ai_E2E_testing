import { test as setup, Page } from '@playwright/test';
import * as path from 'path';
import * as fs from 'fs';

/**
 * Auth Setup — authenticates once and saves session for all tests.
 *
 * Flow:
 *   Navigate to app → React renders login form → fill credentials → save session
 *
 * The app always redirects unauthenticated users to /login.
 * We wait for the login form to render before filling credentials.
 */

const AUTH_FILE = path.join(__dirname, '../.auth/admin.json');

setup('authenticate as admin', async ({ page }) => {
  const email    = process.env.ADMIN_EMAIL    ?? 'reem_user';
  const password = process.env.ADMIN_PASSWORD ?? 'FaRe12345!!';

  // Navigate to app — will redirect to /login
  await page.goto('/', { waitUntil: 'commit', timeout: 30_000 });

  // Wait for React to render the login form
  // Using role-based selector — more resilient than CSS selectors
  const emailInput    = page.getByRole('textbox').first();
  const passwordInput = page.getByLabel(/password/i);
  const submitButton  = page.getByRole('button', { name: /sign in|log in|submit/i })
                            .or(page.locator('button[type="submit"]'));

  await emailInput.waitFor({ state: 'visible', timeout: 30_000 });

  // Fill credentials and submit
  await emailInput.fill(email);
  await passwordInput.fill(password);
  await submitButton.click();

  // Wait for successful redirect to authenticated area
  await page.waitForURL(
    (url) => !url.pathname.includes('/login'),
    { timeout: 30_000 }
  );

  // Save session for all tests
  fs.mkdirSync(path.dirname(AUTH_FILE), { recursive: true });
  await page.context().storageState({ path: AUTH_FILE });
  console.log('✅ Auth state saved');
});
