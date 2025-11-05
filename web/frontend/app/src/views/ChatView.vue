<script setup lang="ts">
import ChatContents from '@/components/ChatContents.vue';
import ChatInput from '@/components/ChatInput.vue';
import type { ChatCommand, ChatMessage, WSResponse, ToolCall } from '@/types';
import { onMounted, ref } from 'vue';

const protocol = window.location.protocol === 'https:' ? 'wss' : 'ws';
const host = window.location.host; // includes hostname + port
const path = window.location.pathname.replace(/\/$/, "");

const loading = ref(true);
const generating = ref(false);

let ws: WebSocket | null = null;

function appendMessage(data: WSResponse) {
    console.log("Received data:", data);
    if ((data.kind === 'text' || data.kind === 'reasoning') && (messages.value.length > 0 && messages.value[messages.value.length -1]!.role !== 'assistant' || messages.value[messages.value.length -1]!.tool_calls != undefined)) {
        messages.value.push({ role: 'assistant', content: '' });
    }
    if (data.kind === 'text') {
        // Handle incoming text chunk
        if (messages.value.length > 0) {
            const lastMessage = messages.value[messages.value.length - 1];
            if (lastMessage!.role === 'assistant') {
                lastMessage!.content += data.text;
            }
        }
    } else if (data.kind === 'reasoning') {
        if (messages.value.length > 0) {
            const lastMessage = messages.value[messages.value.length - 1];
            if (lastMessage!.role === 'assistant') {
                if (!lastMessage!.reasoning) {
                    lastMessage!.reasoning = '';
                }
                lastMessage!.reasoning += data.reasoning;
            }
        }
    } else if (data.kind === 'tool_calls') {
        if (messages.value.length > 0) {
            // add a message with tool calls
            messages.value.push({ role: 'assistant', tool_calls: data.tool_calls, content: '' });
        }
    } else if (data.kind === 'tool_result') {
        if (messages.value.length > 0) {
            messages.value.push({ role: 'tool', tool_call_id: data.tool_call_id!, content: data.content! });
        }
    } else if (data.kind === 'done') {
        // Handle completion
        loading.value = false;
        generating.value = false;
    }
}

function connectWebSocket() {
    ws = new WebSocket(`${protocol}://${host}${path}/api/chat`);
    ws.onopen = () => {
        console.log('WebSocket connected');
        loading.value = false;
        generating.value = false;
        ws?.send(JSON.stringify({ kind: "restore", messages: messages.value }) );
    };
    ws.onclose = () => {
        console.log('WebSocket connection closed');
        loading.value = true;
        generating.value = false;
        setTimeout(() => {
            console.log('Reconnecting WebSocket...');
            connectWebSocket();
        }, 1000);
    };
    ws.onerror = (event) => {
        console.error('WebSocket error:', event);
        loading.value = true;
        generating.value = false;
        ws?.close();
    };
    ws.onmessage = (event: MessageEvent) => {
        const data: WSResponse = JSON.parse(event.data);
        appendMessage(data);
    };
}

onMounted(() => {
    connectWebSocket();
});

function sendMessage(message: string) {
    loading.value = true;
    generating.value = true;
    messages.value.push({ role: 'user', content: message });
    messages.value.push({ role: 'assistant', content: '' }); // Placeholder for assistant response
    const message_to_send: ChatCommand = { kind: "message", message: { role: "user", content: message } };
    ws?.send(JSON.stringify(message_to_send));
}

function sendStop() {
    ws?.send(JSON.stringify({ kind: "stop" }));
}

const messages = ref<Array<ChatMessage>>([]);
</script>

<template>
    <main>
        <div class="chat-container">
            <ChatContents :messages="messages" />
            <ChatInput :loading="loading" :generating="generating" @send-message="sendMessage" @stop="sendStop"/>
        </div>
    </main>
</template>

<style scoped>
main {
    display: flex;
    flex-direction: column;
    align-items: center;
    height: 100%;
    overflow: hidden;
}

.chat-container {
    display: flex;
    flex-direction: column;
    height: 100%;
    max-width: 800px;
    width: 100%;
}
</style>