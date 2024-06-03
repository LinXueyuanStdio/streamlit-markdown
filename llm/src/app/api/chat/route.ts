import { GoogleGenerativeAI } from '@google/generative-ai';
import { GoogleGenerativeAIStream, Message, StreamingTextResponse } from 'ai';

const genAI = new GoogleGenerativeAI(process.env.GOOGLE_API_KEY || '');

// IMPORTANT! Set the runtime to edge
export const runtime = 'edge';

async function savePromptToDatabase(prompt: string) {
  // Save the prompt to your database
}

async function saveCompletionToDatabase(completion: string) {
  // Save the completion to your database
}
const buildGoogleGenAIPrompt = (messages: Message[]) => ({
  contents: messages
    .filter(message => message.role === 'user' || message.role === 'assistant')
    .map(message => ({
      role: message.role === 'user' ? 'user' : 'model',
      parts: [{ text: message.content }],
    })),
});
export async function POST(req: Request) {
  // Extract the `prompt` from the body of the request
  const { messages, token, model = 'gemini-pro', prompt } = await req.json();
  console.log(messages)
  console.log(prompt)

  // Ask Google Generative AI for a streaming completion given the prompt
  const response = await genAI
    .getGenerativeModel({ model })
    .generateContentStream(buildGoogleGenAIPrompt(messages)
      // contents: [{ role: 'user', parts: [{ text: prompt }] }],
    );
  // Convert the response into a friendly text-stream
  const stream = GoogleGenerativeAIStream(response, {
    onStart: async () => {
      // This callback is called when the stream starts
      // You can use this to save the prompt to your database
      await savePromptToDatabase(prompt);
    },
    onToken: async (token: string) => {
      // This callback is called for each token in the stream
      // You can use this to debug the stream or save the tokens to your database
      console.log(token);
    },
    onCompletion: async (completion: string) => {
      // This callback is called when the completion is ready
      // You can use this to save the final completion to your database
      await saveCompletionToDatabase(completion);
    },
  });

  // Respond with the stream
  return new StreamingTextResponse(stream);
}