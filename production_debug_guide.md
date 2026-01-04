# 🕵️ Production Environment Debugging Guide - Three-Layer Diagnosis

## 📋 Current Status Check

Based on code inspection, the following configurations are **already correct**:
- ✅ CORS Configuration: `allow_origins=["*"]` is set
- ✅ Avatar Path: `/static/avatar.png` is correct
- ✅ API Connection: `API_BASE = window.location.origin` auto-adapts to production

---

## 🔍 Layer 1: Exclude Browser Cache Issues

### Symptoms
- Avatar shows as broken image (even though backend sends correctly)
- Frontend displays old error messages
- Status updates not timely

### Solutions

#### Method 1: Force Refresh (Recommended)
1. Open `https://missfay.tonetown.ai` in browser
2. Press `Ctrl + F5` (Windows) or `Cmd + Shift + R` (Mac)
3. This forces browser to reload all resources, ignoring cache

#### Method 2: Incognito Mode Test
1. Open browser incognito/private mode
   - Chrome/Edge: `Ctrl + Shift + N`
   - Firefox: `Ctrl + Shift + P`
   - Safari: `Cmd + Shift + N`
2. Visit `https://missfay.tonetown.ai`
3. Check if avatar and features work normally

#### Method 3: Clear Browser Cache
1. Open browser settings
2. Clear browsing data/cache
3. Revisit the website

### Technical Verification
- ✅ Avatar path confirmed: `/static/avatar.png`
- ✅ Static file mount confirmed: `app.mount("/static", StaticFiles(directory="static"), name="static")`

---

## 🌐 Layer 2: CORS Cross-Origin Check

### Symptoms
- Frontend shows "LLM: ERROR"
- Browser console shows CORS errors
- Network requests blocked by browser

### Current Configuration Check

CORS configuration in **voice_bridge.py**:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ✅ Already allows all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Verification Steps

1. **Open Browser Developer Tools**
   - Press `F12` or Right-click → Inspect
   - Switch to "Console" tab

2. **Check for CORS Errors**
   - Look for red error messages
   - Find errors containing "CORS", "Access-Control", or "blocked"

3. **Check Network Requests**
   - Switch to "Network" tab
   - Refresh page
   - Find requests to `/health` or `/chat`
   - Check request status codes:
     - `200 OK` = Success
     - `CORS error` = Cross-origin issue
     - `404` = Path error
     - `500` = Server error

### If CORS Errors Found

Although code has `allow_origins=["*"]` configured, if issues persist:

1. **Confirm Middleware Order**
   - CORS middleware must be before other middlewares

2. **Check Railway Environment Variables**
   - Confirm no other proxy or reverse proxy config interfering

3. **Temporary Test: Allow Specific Domains**
   ```python
   allow_origins=[
       "https://missfay.tonetown.ai",
       "https://*.tonetown.ai",
       "http://localhost:8000"  # Local testing
   ]
   ```

---

## 🔌 Layer 3: API Endpoint Self-Check

### Test Steps

#### Step 1: Test `/verify-keys` Endpoint

Directly visit in browser:
```
https://missfay.tonetown.ai/verify-keys
```

**Expected Result:**
```json
{
  "status": "healthy",
  "keys": {
    "GEMINI_API_KEY": {
      "exists": true,
      "valid": true,
      "length": 39
    },
    "CARTESIA_API_KEY": {
      "exists": true,
      "valid": true,
      "length": 29
    },
    "CARTESIA_VOICE_ID": {
      "exists": true,
      "valid": true,
      "value": "a5a8b420-9360-4145-9c1e-db4ede8e4b15"
    },
    "GEMINI_MODEL": {
      "exists": true,
      "valid": true,
      "value": "gemini-2.0-flash-exp"
    }
  }
}
```

**If JSON is displayed:**
- ✅ Backend is completely normal
- ✅ API Keys loaded correctly
- ✅ Problem is in frontend HTML/JS connection

**If cannot access:**
- ❌ Railway port mapping may not be active
- ❌ Service may not be started
- ❌ Need to check Railway deployment logs

#### Step 2: Test `/health` Endpoint

Visit in browser:
```
https://missfay.tonetown.ai/health
```

**Expected Result:**
```json
{
  "status": "ok",
  "brain_ready": true,
  "brain_status": "ready",
  "cartesia_status": "ready",
  "engine": "cartesia",
  "timestamp": "2026-01-04T09:30:00.000000"
}
```

**Key Fields:**
- `brain_ready: true` = LLM initialized ✅
- `brain_status: "ready"` = LLM service normal ✅
- `cartesia_status: "ready"` = TTS service normal ✅

#### Step 3: Test Frontend Connection

1. **Open Browser Developer Tools** (F12)
2. **Switch to Console tab**
3. **Type in console:**
   ```javascript
   fetch('https://missfay.tonetown.ai/health')
     .then(r => r.json())
     .then(data => console.log('Health:', data))
     .catch(e => console.error('Error:', e))
   ```

**If successful:**
- Console shows health status JSON
- ✅ Frontend can connect to backend

**If failed:**
- Console shows error message
- Check error type (CORS, network, timeout, etc.)

---

## 🛠️ Quick Diagnosis Checklist

### ✅ Completed Checks

- [x] CORS middleware configured: `allow_origins=["*"]`
- [x] Avatar path correct: `/static/avatar.png`
- [x] API base URL auto-adapts: `window.location.origin`
- [x] Static files mounted correctly: `/static` endpoint

### 🔍 User Verification Needed

- [ ] Browser force refresh (Ctrl + F5)
- [ ] Incognito mode test
- [ ] `/verify-keys` endpoint accessible
- [ ] `/health` endpoint returns `brain_ready: true`
- [ ] No CORS errors in browser console
- [ ] Network request status code is 200

---

## 📞 If Problems Persist

### Collect Diagnostic Information

1. **Browser Console Errors**
   - Screenshot or copy all red error messages

2. **Network Request Details**
   - Open Network tab
   - Find failed requests
   - View Request Headers and Response

3. **Railway Deployment Logs**
   - Download latest logs from Railway Dashboard
   - Look for startup errors or runtime errors

4. **Health Check Results**
   - Full JSON response from `/health` and `/verify-keys`

### Common Issues Troubleshooting

| Symptom | Possible Cause | Solution |
|---------|---------------|----------|
| Broken avatar | Browser cache | Ctrl + F5 force refresh |
| LLM: ERROR | CORS issue | Check browser console |
| LLM: ERROR | Backend not started | Check Railway logs |
| Cannot access | Port mapping | Wait for Railway deployment |
| 500 error | Code error | Check Railway logs |

---

## 🎯 Expected Final State

When all issues are resolved, you should see:

1. ✅ Avatar displays normally
2. ✅ Top-right shows "LLM: OK" and "TTS: OK"
3. ✅ Can send messages and receive replies normally
4. ✅ Audio plays normally
5. ✅ `/health` returns `brain_ready: true`
6. ✅ `/verify-keys` shows all keys valid

---

**Last Updated:** 2026-01-04
**Status:** Awaiting user verification

