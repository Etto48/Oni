export type ChatMessage = {
    role: "system" | "user" | "assistant" | "tool";
    tool_calls?: ToolCall[];
    tool_call_id?: string;
    reasoning?: string;
    content: string;
}

export type ChatCommand = {
    kind: "message" | "stop" | "restore";
    message?: ChatMessage;
    messages?: ChatMessage[];
}

export type ToolCall = {
    id: string;
    function: { name: string; arguments: any; };
}

export type WSResponse = {
    kind: "text" | "reasoning" | "tool_calls" | "done" | "tool_result";
    text?: string;
    reasoning?: string;
    tool_calls?: ToolCall[];
    tool_call_id?: string;
    content?: string;
}