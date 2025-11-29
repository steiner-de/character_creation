# Google Service Account JSON Setup

## What is a Service Account JSON?

A service account JSON file is a credentials file that allows your application to authenticate with Google Cloud APIs without user interaction. It contains a private key and metadata needed to access your Google Cloud project's resources.

## Structure of service_account.json

Here's what a typical service account JSON file looks like:

```json
{
  "type": "service_account",
  "project_id": "your-project-id-12345",
  "private_key_id": "abc123def456ghi789jkl012",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC7VJTUt9Us8cKj\n...\n-----END PRIVATE KEY-----\n",
  "client_email": "character-creator@your-project-id-12345.iam.gserviceaccount.com",
  "client_id": "123456789012345678901",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/character-creator%40your-project-id-12345.iam.gserviceaccount.com"
}
```

### Field Explanations

| Field | Description |
|-------|-------------|
| `type` | Always `"service_account"` for service accounts |
| `project_id` | Your Google Cloud project ID (found in GCP console) |
| `private_key_id` | Unique identifier for the private key |
| `private_key` | The actual private key (multiline, contains newlines) |
| `client_email` | Service account email address |
| `client_id` | Unique numeric ID for the service account |
| `auth_uri` | OAuth 2.0 authorization server URL |
| `token_uri` | OAuth 2.0 token endpoint URL |
| `auth_provider_x509_cert_url` | URL to Google's public certificates |
| `client_x509_cert_url` | URL to this service account's certificates |

## How to Create a Service Account

### Step 1: Create a Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click the project dropdown at the top
3. Click "NEW PROJECT"
4. Enter project name (e.g., "Character Creator")
5. Click "CREATE"

### Step 2: Enable Required APIs

1. In the GCP Console, go to **APIs & Services** → **Library**
2. Search for and enable these APIs:
   - **Google Docs API**
   - **Google Drive API**
   - **Vertex AI API**

### Step 3: Create a Service Account

1. Go to **APIs & Services** → **Credentials**
2. Click **Create Credentials** → **Service Account**
3. Fill in the form:
   - **Service account name:** e.g., "character-creator"
   - **Service account ID:** Auto-filled based on name
   - Click **CREATE AND CONTINUE**
4. Grant roles (click **Continue** if not shown):
   - Select **Basic** → **Editor** (or more specific roles below)
   - Click **Continue**

### Step 4: Create and Download the JSON Key

1. On the Service Account page, click the **Keys** tab
2. Click **Add Key** → **Create new key**
3. Choose **JSON** as the key type
4. Click **CREATE**
5. The JSON file will automatically download as `your-service-account-name.json`

### Step 5: Configure Your Project

1. Move the downloaded JSON to your project directory:
   ```
   character_creation/service_account.json
   ```

2. Update your `.env` file:
   ```
   GOOGLE_APPLICATION_CREDENTIALS=service_account.json
   GOOGLE_PROJECT=your-project-id
   GOOGLE_LOCATION=us-central1
   GEMINI_MODEL=text-bison@001
   CHARACTERS_CSV=characters.csv
   ```

## Required Permissions

Your service account needs these IAM roles:

| API | Required Role | Scope |
|-----|---------------|-------|
| Google Docs API | `roles/editor` | Create, edit, read documents |
| Google Drive API | `roles/editor` | Create, upload files |
| Vertex AI | `roles/aiplatform.user` | Access Gemini models |

### Granular Alternative (if not using Editor role)

Instead of Editor, you can assign these specific roles:

- `roles/docs.editor` - Edit Google Docs
- `roles/drive.file` - Manage files created by the service account
- `roles/aiplatform.user` - Use Vertex AI models

## Minimal service_account.json Example

If you're testing and need a reference, here's the minimal structure (DON'T use these fake values):

```json
{
  "type": "service_account",
  "project_id": "my-character-project",
  "private_key_id": "1",
  "private_key": "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n",
  "client_email": "character-creator@my-character-project.iam.gserviceaccount.com",
  "client_id": "1234567890",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/character-creator%40my-character-project.iam.gserviceaccount.com"
}
```

## Security Best Practices

⚠️ **IMPORTANT:**

1. **Never commit to git**: Add `service_account.json` to `.gitignore` (already done)
2. **Never share publicly**: This file has your private key
3. **Keep it safe**: Treat it like a password
4. **Rotate keys periodically**: Generate new keys and disable old ones in GCP
5. **Use environment variables**: Keep the path in `.env` file, not hardcoded

## Troubleshooting

### "Permission denied" error
- Ensure the service account has been granted the required roles
- Wait a few minutes for role propagation in GCP

### "API not enabled" error
- Go to **APIs & Services** → **Library**
- Search for the API
- Click **ENABLE**

### "Invalid key format" error
- Ensure the JSON is properly formatted
- Check that `private_key` field contains the full key with newlines
- Don't modify the JSON file manually

## Testing Your Setup

Once you have the service account JSON, test with:

```powershell
# Activate virtual environment first
.\setup_venv.ps1

# Create a simple test
python -c "from src.gdocs import create_services; drive, docs = create_services('service_account.json'); print('✅ Authentication successful!')"
```

If successful, you'll see `✅ Authentication successful!`
