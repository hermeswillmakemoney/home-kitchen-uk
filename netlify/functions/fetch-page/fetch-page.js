// Netlify Function: fetch-page
// Proxies requests to bypass IP-based bot detection
// Usage: GET /.netlify/functions/fetch-page?url=https://example.com

export default async (req) => {
  const url = new URL(req.url).searchParams.get('url');
  
  if (!url) {
    return new Response(JSON.stringify({ error: 'Missing ?url= parameter' }), {
      status: 400,
      headers: { 'Content-Type': 'application/json' }
    });
  }

  // Only allow specific domains
  const allowed = [
    'argos.co.uk', 'www.argos.co.uk',
    'currys.co.uk', 'www.currys.co.uk', 
    'johnlewis.com', 'www.johnlewis.com',
    'ao.com', 'www.ao.com',
    'lakeland.co.uk', 'www.lakeland.co.uk',
    'very.co.uk', 'www.very.co.uk',
    'amazon.co.uk', 'www.amazon.co.uk',
    'ebay.co.uk', 'www.ebay.co.uk',
    'which.co.uk', 'www.which.co.uk',
    'trustedreviews.com', 'www.trustedreviews.com',
    'techradar.com', 'www.techradar.com',
    't3.com', 'www.t3.com',
  ];

  try {
    const targetUrl = new URL(url);
    const hostname = targetUrl.hostname;
    if (!allowed.includes(hostname)) {
      return new Response(JSON.stringify({ error: `Domain ${hostname} not allowed` }), {
        status: 403,
        headers: { 'Content-Type': 'application/json' }
      });
    }
  } catch {
    return new Response(JSON.stringify({ error: 'Invalid URL' }), {
      status: 400,
      headers: { 'Content-Type': 'application/json' }
    });
  }

  try {
    const response = await fetch(url, {
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-GB,en;q=0.9,en-US;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Cache-Control': 'no-cache',
        'Pragma': 'no-cache',
        'Sec-Ch-Ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
      },
      redirect: 'follow',
    });

    const body = await response.text();

    return new Response(JSON.stringify({
      status: response.status,
      url: response.url,
      headers: Object.fromEntries(response.headers.entries()),
      body: body.substring(0, 500000), // 500KB cap
      truncated: body.length > 500000,
    }), {
      headers: { 
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
      }
    });
  } catch (error) {
    return new Response(JSON.stringify({ error: error.message }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' }
    });
  }
};

export const config = {
  path: "/api/fetch",
};
