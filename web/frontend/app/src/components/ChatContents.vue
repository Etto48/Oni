<script setup lang="ts">
import type { ChatMessage } from '@/types';
import { ref, watch } from 'vue';

const props = defineProps<{
    messages: Array<ChatMessage>;
}>();

const autoScroll = ref(true);
const chatContentsRef = ref<HTMLElement | null>(null);

watch(
    props.messages,
    () => {
        if (autoScroll.value && chatContentsRef.value) {
            chatContentsRef.value.scrollTop = chatContentsRef.value.scrollHeight;
        }
    },
    { deep: true }
);

function handleScroll(event: Event) {
    // set autoScroll to false if user scrolls up
    const target = event.target as HTMLElement;
    autoScroll.value = target.scrollTop + target.clientHeight >= target.scrollHeight - 10;
}

</script>

<template>
    <div class="chat-contents" ref="chatContentsRef" @scroll="handleScroll">
        <div
            v-for="(message, index) in messages.filter(m => m.role !== 'system')"
            :key="index"
            :class="['message', message.role]"
        >
            <div class="message-content">
                {{ message.content }}
            </div>
        </div>
    </div>
</template>

<style scoped>
.chat-contents {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    padding: 1rem;
    flex: 1;
    overflow-y: auto;
}
.message {
    max-width: 70%;
    padding: 0.75rem 1rem;
    border-radius: 0.5rem;
    word-wrap: break-word;
}
.message.user {
    align-self: flex-end;
    background-color: var(--color-border);
    color: var(--color-text-strong);
}

.message.assistant {
    align-self: flex-start;

}
</style>