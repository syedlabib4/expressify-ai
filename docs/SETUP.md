# Application setup

This public repository contains the portfolio showcase, not the application source. These instructions document how to run Expressify AI from an authorized full source checkout. The screenshot GIF can be rebuilt from this repository using the last section below.

## Prerequisites

| Requirement | Project configuration |
| --- | --- |
| Node.js | 22.11 or later; hosted backend uses 22.x |
| Package manager | npm with the source lockfiles |
| Java | JDK 17 |
| Android tooling | Android Studio, SDK platform tools and an authorized USB-debugging phone |
| Android SDK | Minimum 24, compile 37, target 36 |
| Build tools / NDK | 37.0.0 / 27.1.12297006 |
| Gradle / Kotlin | Wrapper 9.4.1 / 2.2.0 |
| Database | MongoDB Atlas or another transaction-capable deployment |
| Optional AI | Backend-only Gemini API key |

Android is the supported sensing platform. The iOS project does not yet provide verified native sensing parity and requires macOS/Xcode work.

## 1 Install dependencies

From the application root, which contains `package.json`, `android`, `src`, and `backend`:

```powershell
npm ci
Push-Location backend
npm ci
Copy-Item .env.example .env
Pop-Location
```

Edit `backend/.env` locally. A configuration shape is shown below; replace placeholders on your own machine.

```dotenv
PORT=5000
MONGODB_URI=mongodb+srv://USERNAME:PASSWORD@YOUR_CLUSTER/expressify
JWT_SECRET=REPLACE_WITH_A_LONG_RANDOM_SECRET
GEMINI_API_KEY=
```

Use a unique random JWT secret of at least 32 characters for production. Keep secrets out of Git, screenshots, command output, and client configuration. Gemini is optional for the current core activities.

MongoDB transactions are required for scored completion receipts. If using Atlas, configure its network access and database permissions appropriately. Do not run a curriculum seed against an existing learner database to change content; the level seed replaces definitions.

## 2 Connect and launch Android

Enable Developer options and USB debugging on one Android phone. Connect the cable and accept the phone's authorization prompt.

```powershell
adb devices
powershell -ExecutionPolicy Bypass -File .\start-android.ps1 -Install
```

The launch script starts missing local services, waits for readiness, restores USB forwarding, and opens the installed app. After an initial install, reconnect with:

```powershell
powershell -ExecutionPolicy Bypass -File .\start-android.ps1
```

The debug app requires Metro. Local account features also require the backend and its database connection. Reconnect forwarding after unplugging USB.

### Manual startup

Start Metro in one terminal:

```powershell
npm start
```

Start the backend in another:

```powershell
Set-Location backend
npm start
```

Then restore forwarding and launch from the app root:

```powershell
adb reverse tcp:8081 tcp:8081
adb reverse tcp:5000 tcp:5000
npm run android -- --no-packager
```

The default API is `http://localhost:5000/api`; the administrator dashboard is served at `http://localhost:5000/dashboard/`. The health route is `/api/health` and checks database readiness.

## 3 Select a different API endpoint

Set the build-time endpoint before Metro starts or the APK is built:

```powershell
$env:EXPRESSIFY_API_BASE_URL = 'http://10.0.2.2:5000/api'
npm start -- --reset-cache
```

The example is an Android emulator host address. A physical phone using USB forwarding can use localhost. A phone using Wi-Fi needs a reachable LAN address or a hosted HTTPS endpoint. URLs must end in `/api` and contain no credentials, fragments or query parameters.

## 4 Verify the source checkout

```powershell
npm test -- --runInBand
npx tsc --noEmit
npm run lint -- --quiet
Push-Location backend
npm test
Pop-Location
```

Backend database integration tests are opt-in and use an isolated database. They should follow the application backend README, with suitable test credentials. A passing unit suite alone does not validate physical camera/speech performance or child usability.

## 5 Standalone QA and release

The QA variant uses `com.faceanalyzer.qa`, bundles JavaScript and models, and opens without Metro. It uses an internal debug signing key. Account-dependent saving still needs a reachable backend.

```powershell
# From the application source root
.\tools\prepare-vercel.ps1
# Review/deploy the separate backend package with private server configuration.
.\tools\build-hosted-qa.ps1
adb install -r .\android\app\build\outputs\apk\qa\app-qa.apk
```

The hosted backend package targets Vercel Express hosting and MongoDB Atlas. Set `NODE_ENV`, `MONGODB_URI`, `JWT_SECRET`, and optionally `GEMINI_API_KEY` in the hosting environment. Verify health and protected-route authorization before distributing a QA APK.

Production distribution additionally requires a release-owner keystore and an HTTPS API. The source build expects `EXPRESSIFY_RELEASE_STORE_FILE`, `EXPRESSIFY_RELEASE_STORE_PASSWORD`, `EXPRESSIFY_RELEASE_KEY_ALIAS`, and `EXPRESSIFY_RELEASE_KEY_PASSWORD`. Supply them through a local/CI secret mechanism, not a public file. Internal QA installation is separate from Play Store readiness.

## Troubleshooting

| Symptom | Check |
| --- | --- |
| Phone not listed | Cable, USB debugging, the authorization prompt, and `adb devices` |
| Debug app cannot load JavaScript | Metro on 8081 and USB forwarding |
| Login or sync fails | Backend health, Atlas connectivity/network access and endpoint configuration |
| Camera or microphone unavailable | Permission settings; use picture/watch-first alternatives |
| Voice unavailable | Installed Android English TTS voice; keep visible text/picture alternatives |
| Windows native path-length failures | Use a short source checkout path; do not overwrite an existing directory |
| Old API endpoint remains in a build | Set the environment before bundling and restart Metro with cache reset |

## Rebuild the showcase tour

This step works from this public repository and does not require application source:

```powershell
python -m pip install Pillow
python tools/build_tour.py
```

The script reads the five screenshots and writes `docs/media/expressify-tour.gif`. It never connects to a phone or records camera/audio.
