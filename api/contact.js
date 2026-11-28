// Vercel serverless function: emails contact-form enquiries via Resend.
// Env vars (Vercel -> Project -> Settings -> Environment Variables):
//   RESEND_API_KEY  required  API key from https://resend.com
//   CONTACT_TO      optional  recipient (default info@blueharboradvisory.com)
//   RESEND_FROM     optional  sender, must be on a Resend-verified domain
//                             (default "BlueHarbor Website <onboarding@resend.dev>")

const esc = (s) =>
  String(s).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));

const clean = (v, max) => (typeof v === 'string' ? v.replace(/[\r\n]+/g, ' ').trim().slice(0, max) : '');

module.exports = async (req, res) => {
  res.setHeader('Cache-Control', 'no-store');
  if (req.method !== 'POST') {
    res.setHeader('Allow', 'POST');
    return res.status(405).json({ success: false, message: 'Method not allowed' });
  }

  const body = typeof req.body === 'string' ? safeParse(req.body) : req.body || {};

  // Honeypot: real visitors never fill this hidden field.
  if (body.website) return res.status(200).json({ success: true });

  const name = clean(body.name, 120);
  const organisation = clean(body.organisation, 160);
  const email = clean(body.email, 160);
  const phone = clean(body.phone, 60);
  const type = clean(body.type, 60) || 'Not specified';
  const service = clean(body.service, 160) || 'Not specified';
  const message = typeof body.message === 'string' ? body.message.trim().slice(0, 5000) : '';

  if (name.length < 2 || message.length < 2 || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
    return res.status(400).json({ success: false, message: 'Please complete the required fields.' });
  }

  const apiKey = process.env.RESEND_API_KEY;
  if (!apiKey) {
    return res.status(500).json({ success: false, message: 'Email delivery is not configured yet.' });
  }

  const rows = [
    ['Name', name],
    ['Organisation', organisation || '—'],
    ['Email', email],
    ['Phone', phone || '—'],
    ['Reaching out as', type],
    ['Area of interest', service],
  ];
  const html =
    `<h2 style="font-family:sans-serif">New mandate enquiry</h2>` +
    `<table style="font-family:sans-serif;border-collapse:collapse">` +
    rows.map(([k, v]) => `<tr><td style="padding:4px 16px 4px 0;color:#555"><b>${k}</b></td><td>${esc(v)}</td></tr>`).join('') +
    `</table><h3 style="font-family:sans-serif">Message</h3>` +
    `<p style="font-family:sans-serif;white-space:pre-wrap">${esc(message)}</p>`;
  const text = rows.map(([k, v]) => `${k}: ${v}`).join('\n') + `\n\n${message}`;

  try {
    const r = await fetch('https://api.resend.com/emails', {
      method: 'POST',
      headers: { Authorization: `Bearer ${apiKey}`, 'Content-Type': 'application/json' },
      body: JSON.stringify({
        from: process.env.RESEND_FROM || 'BlueHarbor Website <onboarding@resend.dev>',
        to: [process.env.CONTACT_TO || 'info@blueharboradvisory.com'],
        reply_to: email,
        subject: `New mandate enquiry — ${type} — ${service}`,
        html,
        text,
      }),
    });
    if (!r.ok) {
      console.error('Resend error', r.status, await r.text());
      return res.status(502).json({ success: false, message: 'Could not send the email.' });
    }
    return res.status(200).json({ success: true });
  } catch (err) {
    console.error('Contact function error', err);
    return res.status(502).json({ success: false, message: 'Could not send the email.' });
  }
};

function safeParse(s) {
  try { return JSON.parse(s); } catch { return {}; }
}
