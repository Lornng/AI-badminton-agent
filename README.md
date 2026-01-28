# AI-badminton-agent

This is a web deployment for the porposal generator
Details workflow will be below


Workflow
1. Create a testing agent from Elevenlabs
2. n8n (webhook >  AI agent > trim the output and then genreeate the output in proper JSON object format)
3. Prepare a website the bussiness proposal deployment (antigravity & render) (other IDE or deployment steps can be taken)
4. n8n (http POST request to the web)
5. n8n (send this generated proposal to the client's email address)
