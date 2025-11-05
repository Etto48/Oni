export type ChatCommandMessage = {
    kind: "message";
} & ChatMessage;

export type ChatMessage = {
    role: "system" | "user" | "assistant";
    content: string;
}

export type ChatCommandStop = {
    kind: "stop";
};

export type ChatCommandRestore = {
    kind: "restore";
    messages: ChatMessage[];
};

export type ChatCommand = ChatCommandMessage | ChatCommandStop | ChatCommandRestore;

export type WSResponse =
    WSResponseText | WSResponseDone;

export type WSResponseText = {
    kind: "text";
    text: string;
};

export type WSResponseDone = {
    kind: "done";
};