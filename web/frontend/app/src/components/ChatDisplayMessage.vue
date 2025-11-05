<script setup lang="ts">
import type { ChatMessage } from '@/types';
import { Settings, Dot } from 'lucide-vue-next';
defineProps<{
    message: ChatMessage;
}>();
</script>

<template>
    <div
        :class="['message', message.role]"
    >
        <div v-if="message.role === 'assistant' && message.reasoning" class="reasoning-wrapper">
            <details class="reasoning" :open="false">
                <summary>Reasoning</summary>
                <div class="reasoning-content">{{ message.reasoning }}</div>
            </details>
        </div>
        <details v-if="message.role === 'tool'">
            <summary>Result</summary>
            <div class="tool-result">{{ message.content }}</div>
        </details>
        <div v-if="message.role !== 'tool' && message.content" class="message-content">{{ message.content }}</div>
        <div v-if="message.tool_calls" class="tool-calls">
            <div
                v-for="(toolCall, tcIndex) in message.tool_calls"
                :key="tcIndex"
                class="tool-call"
            >
                <details>
                <summary><Settings /><strong>{{ toolCall.function.name }}</strong></summary>
                <div>
                    <strong>Arguments:</strong>
                    <div v-for="(argValue, argName) in JSON.parse(toolCall.function.arguments)" :key="argName" class="call-args">
                        <em><Dot />{{ argName }}:</em>{{ argValue }}
                    </div>
                </div>
                </details>
            </div>
        </div>
    </div>
</template>

<style scoped>
.call-args {
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.call-args em {
    display: flex;
    align-items: center;
}

.tool-call {
    padding: 0.5rem;
    background-color: var(--color-background-soft);
    border-radius: 8px;
}

.tool-call summary {
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.tool-call details[open] summary {
    margin-bottom: 0.5rem;
}

.tool-call strong {
    font-weight: 600;
}

.tool-call svg {
    color: var(--color-text-strong);
    opacity: 0.7;
    height: 20px;
    width: 20px;
}

.reasoning-wrapper {
    background-color: var(--color-background-mute);
    border-radius: 10px;
    padding: 0.5rem;
    width: fit-content;
    transition: all 0.3s ease;
}

.reasoning-content {
    padding: 0.5rem;
}

summary {
    cursor: pointer;
}

details[open] summary {
    margin-bottom: 0.5rem;
}
.message {
    box-sizing: border-box;
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    max-width: 100%;
    border-radius: 0.5rem;
    word-wrap: break-word;
}
.message.user {
    align-self: flex-end;
    padding: 0.75rem 1rem;
    background-color: var(--color-border);
    color: var(--color-text-strong);
}

.message.assistant, .message.tool {
    align-self: flex-start;

}
</style>