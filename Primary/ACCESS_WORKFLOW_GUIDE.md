# Admin & Student Access Workflow 🛡️🎓

This guide explains how you (the Admin) maintain **Full Control** over the platform.

---

## 1. The Student Workflow (Signing Up)
1.  **Student Action**: On the login page, the student clicks **"Request New Access"**.
2.  **Details Provided**: They enter their **Name**, **Parent's Name**, and **Grade**.
3.  **Temporary Token**: The app generates a professional sequential token (e.g., `PSK00001`).
4.  **Access Blocked**: If they try to log in immediately, the app says:
    > "Your token is PENDING approval. Please ask your teacher to approve it!"

---

## 2. The Admin Workflow (Approving & Monitoring)
You have total authority to grant or deny access.

### A. Granting Access
1.  **Log In**: Use your master token: `ADMIN100`.
2.  **Approve Requests**: Go to the **"Approve Requests (1) 📝"** tab.
3.  **Telegram Alert**: You will also receive a Telegram message showing the student's name and parents' name.
4.  **Manual Approval**: Click **"Approve"**. Only now can the student log in.

### B. Full Monitoring
1.  **Real-Time Tracking**: Go to the **"Full Monitoring"** tab.
2.  **Comprehensive View**: You see a table mapping:
    *   **Student Name** + **Parent's Name** + **Token** + **Class**.
3.  **Participation**: See exactly which student finished which exam and what their score was.

### C. Revoking Access (The "Delete" Power)
1.  Go to the **"Manage All Tokens"** tab.
2.  Find any student using their token or name.
3.  Click **"Delete/Revoke Token"**. This student is immediately removed from the system.

---

## 3. Summary of Roles

| Feature | Admin (`ADMIN100`) | Student (`PSKxxxxx`) |
| :--- | :--- | :--- |
| **Access Control** | Full (Approve/Delete) | None (Wait for Admin) |
| **Monitoring** | Sees Everyone's Marks | Sees Only Own Marks |
| **Settings** | Can See WiFi/Web URLs | Locked Out |
| **Modules** | Review Mode | Learning Mode |

---
**Your Control:** No student can access the website without your approval. You see everything they do! 🛡️📚
