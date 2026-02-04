# AI-badminton-agent

This is a web deployment for the porposal generator
Details workflow will be below


Workflow
1. Create a testing agent from Elevenlabs
2. n8n (webhook >  AI agent > trim the output and then genreeate the output in proper JSON object format)
3. Prepare a website the bussiness proposal deployment (antigravity & render) (other IDE or deployment steps can be taken)
4. n8n (http POST request to the web)
5. n8n (send this generated proposal to the client's email address)


n8n Workflow (Details)
1. WebHook (Test URL > change Path name)
2. Code in javascript (convert JSON into STRING, so AI Agnet could read it)
```
const trasnscriptArray = $input.first().json.body.data.transcript
let transcript= ""

for (const trans of trasnscriptArray) {
  const role = trans.role || "";
  const message = trans.message || "";

  if (!message) continue;

  if (role == "agent") {
    transcript += " Agent: "+ trans.message;
  }  

  if (role == "user") {
    transcript += " User: "+ trans.message;
  }
}

transcript = transcript.trim();
    
return {
  transcript
}
```
3. AI Agent prompt (generate conversation output)
```
Read in this transcript {{ $json.transcript }}. WWrite me a proposal with the user's name, email and products details required. Store the output in a JSON format. 
```
4. Link a chat model to AI Agent (OpenRouter Chat Model)
5. Code in Javascript (convert STRING output from AI Agent into JSON)
```
// 1️⃣ Get the AI output string
let aiOutput = $input.first().json.output || "";

// 2️⃣ Remove the "```json" prefix and trailing backticks
aiOutput = aiOutput.replace(/^```json/, "").replace(/```$/,"").trim();

// 3️⃣ Parse JSON safely
let parsed = {};
try {
    parsed = JSON.parse(aiOutput);
} catch (err) {
    return [
        { json: { error: "Invalid JSON from AI output", raw: aiOutput } }
    ];
}

// 4️⃣ Extract categories dynamically
const proposal = parsed.proposal || {};
const output = {};

// Loop through top-level keys in proposal
for (const key of Object.keys(proposal)) {
    const value = proposal[key];

    if (Array.isArray(value)) {
        // For arrays, store as array of objects
        output[key] = value.map(item => item);
    } else if (typeof value === "object" && value !== null) {
        // Nested objects → keep as object
        output[key] = value;
    } else {
        // Primitive values → keep as is
        output[key] = value;
    }
}

// 5️⃣ Return the restructured JSON
return [
    { output }
];
```
6. HTTP Request
```
POST METHOD
Send body
Using JSON
```
