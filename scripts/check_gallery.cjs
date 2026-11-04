// Browser checks exercise the HTML previews. They do not execute Power Fx.
const { chromium } = require('playwright');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const { pathToFileURL } = require('node:url');

(async () => {
  const browser = await chromium.launch({ headless: true,
    ...(process.env.BROWSER_EXECUTABLE ? { executablePath: process.env.BROWSER_EXECUTABLE } : {}) });
  const root = path.resolve(__dirname, '..');
  const artifacts = process.env.ARTIFACT_DIR || fs.mkdtempSync(path.join(os.tmpdir(), 'power-apps-preview-'));
  fs.mkdirSync(artifacts, { recursive: true });
  const page = await browser.newPage({ viewport: { width: 1440, height: 1050 }, reducedMotion: 'reduce' });
  const errors = [], requests = [];
  page.setDefaultTimeout(7000);
  page.on('pageerror', error => errors.push(error.message));
  page.on('console', message => { if (message.type() === 'error') errors.push(message.text()); });
  page.on('request', request => { if (/^https?:/.test(request.url())) requests.push(request.url()); });
  const choose = async id => page.viewportSize().width <= 760
    ? page.locator('#gallery-picker').selectOption(id) : page.locator(`[data-show="${id}"]`).click();
  const text = selector => page.locator(selector).innerText();
  try {
    await page.goto(pathToFileURL(path.join(root, 'preview/index.html')).href, { waitUntil: 'networkidle' });
    const ids = await page.locator('[data-component]').evaluateAll(nodes => nodes.map(node => node.id));
    assert.equal(ids.length, 15);
    assert.equal(await page.locator('[data-component]:visible').count(), 15);
    assert.equal(await page.locator('.component-recording img[src$=".gif"]').count(), 0, 'No GIF autoplay');
    await page.locator('#gallery-search').fill('filter');
    assert.equal(await page.locator('[data-component]:visible').count(), 1);
    await page.locator('#gallery-search').fill('no-such-component');
    assert.equal(await page.locator('#gallery-empty').isVisible(), true);
    await page.locator('#gallery-clear').click();

    await choose('form-field');
    assert.equal(await text('#ff-valid'), 'No');
    assert.equal(await text('#ff-error'), '');
    await page.locator('#ff-input').focus();
    await page.keyboard.press('Tab');
    assert.equal(await text('#ff-error'), '', 'Untouched blur stays quiet');
    await page.locator('#ff-show-validation').check();
    assert.match(await text('#ff-error'), /required/);
    await page.locator('#ff-input').fill('Quarterly review');
    assert.equal(await text('#ff-valid'), 'Yes');
    assert.equal(await text('#ff-error'), '');
    await page.keyboard.press('Tab');
    assert.match(await text('#ff-event'), /emitted after blur/);
    await page.locator('#ff-host-error').check();
    assert.equal(await text('#ff-valid'), 'No');
    assert.match(await text('#ff-error'), /already in use/);
    await page.locator('#ff-disabled').check();
    assert.equal(await page.locator('#ff-input').isDisabled(), true);
    await page.locator('#ff-reset').click();
    assert.equal(await page.locator('#ff-input').inputValue(), '');
    assert.equal(await page.locator('#ff-host-error').isChecked(), true, 'Reset preserves host inputs');
    await page.locator('#ff-host-error').uncheck();
    await page.locator('#ff-required').uncheck();
    await page.locator('#ff-disabled').uncheck();
    assert.equal(await text('#ff-valid'), 'Yes');
    await page.locator('#ff-required').check();
    await page.locator('#ff-input').fill('   ');
    assert.equal(await text('#ff-valid'), 'No');
    await page.locator('#ff-input').fill('Quarterly review');
    await page.locator('#form-field').screenshot({ path: path.join(artifacts, 'form-field-preview.png') });

    await choose('search-filter-bar');
    assert.equal(await page.locator('#sf-results li').count(), 6);
    assert.deepEqual(await page.locator('#sf-status option').allTextContents(), ['All statuses', 'Not started', 'In progress', 'Completed']);
    await page.locator('#sf-query').fill('  review  ');
    assert.equal(await page.locator('#sf-results li').count(), 3);
    await page.locator('#sf-status').selectOption('Completed');
    await page.locator('#sf-owner').selectOption('Jordan');
    assert.equal(await page.locator('#sf-results li').count(), 1);
    assert.match(await text('#sf-results'), /Review contrast/);
    assert.match(await text('#sf-summary'), /3 active filters/);
    await page.locator('#sf-owner').selectOption('Alex');
    assert.equal(await page.locator('#sf-empty').isVisible(), true);
    await page.locator('#sf-clear').focus();
    await page.keyboard.press('Enter');
    assert.equal(await page.locator('#sf-results li').count(), 6);
    assert.equal(await page.locator('#sf-query').evaluate(el => el === document.activeElement), true);
    await page.locator('#sf-status').selectOption('Not started');
    assert.equal(await page.locator('#sf-results li').count(), 2);
    await page.locator('#search-filter-bar').screenshot({ path: path.join(artifacts, 'search-filter-bar-preview.png') });
    await page.locator('#sf-clear').click();

    await choose('message-banner');
    for (const intent of ['Info', 'Warning', 'Error', 'Success']) {
      await page.locator('#mb-intent').selectOption(intent);
      assert.equal(await text('#mb-state'), intent);
      assert.equal(await page.locator('#mb-announcement').getAttribute('aria-live'), ['Warning','Error'].includes(intent) ? 'assertive' : 'polite');
    }
    await page.locator('#mb-intent').selectOption('Error');
    await page.locator('#mb-action').focus();
    await page.keyboard.press('Enter');
    assert.equal(await text('#mb-state'), 'Success');
    assert.match(await text('#mb-message'), /No record was saved/);
    await page.locator('#mb-dismiss').click();
    assert.equal(await page.locator('#mb-banner').isVisible(), false);
    assert.equal(await page.locator('#mb-show').evaluate(el => el === document.activeElement), true);
    await page.keyboard.press('Enter');
    assert.equal(await page.locator('#mb-banner').isVisible(), true);
    await page.locator('#mb-dismissible').uncheck();
    assert.equal(await page.locator('#mb-dismiss').isVisible(), false);
    await page.locator('#mb-message-input').fill('Long message '.repeat(60));
    await page.locator('#mb-apply').click();
    assert.equal(await text('#mb-message'), 'Long message '.repeat(60));
    await page.locator('#mb-reset').click();
    await page.locator('#message-banner').screenshot({ path: path.join(artifacts, 'message-banner-preview.png') });

    // Every component must remain readable at narrow and wide page widths.
    for (const width of [1440, 390, 320]) {
      await page.setViewportSize({ width, height: 1050 });
      for (const id of ids) {
        await choose(id);
        assert.equal(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth), true, `${id}: page overflow at ${width}px`);
      }
      await choose('message-banner');
      await page.locator('#mb-message-input').fill('LongWord'.repeat(80));
      await page.locator('#mb-apply').click();
      assert.equal(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth), true, `Long message overflow at ${width}px`);
      if (width === 390) await page.screenshot({ path: path.join(artifacts, 'new-components-mobile.png'), fullPage: true });
      await page.locator('#mb-reset').click();
    }

    for (const id of ['form-field','search-filter-bar','message-banner']) {
      await choose(id);
      await page.locator(`[data-recording="${id}"]`).click();
      await page.waitForFunction(key => { const image = document.querySelector(`#recording-${key} img`); return image.complete && image.naturalWidth > 0; }, id);
      assert.equal(await page.locator('.component-recording img[src$=".gif"]').count(), 1);
      assert.equal(await page.locator(`#${id}>.component-demo`).isVisible(), false);
      await page.locator(`[data-recording="${id}"]`).click();
      assert.equal(await page.locator(`#${id}>.component-demo`).isVisible(), true);
    }
    assert.deepEqual(errors, []);
    assert.deepEqual(requests, []);
    console.log('PASS: field validation, AND filters, message actions, keyboard interactions, GIF controls, and all 15 layouts at 1440/390/320px.');
    console.log('Screenshots: ' + artifacts);
  } finally { await browser.close(); }
})().catch(error => { console.error(error); process.exitCode = 1; });
