<script setup lang="ts">
import { ref, nextTick } from 'vue';
import { ArrowUp, LoaderCircle, Square } from 'lucide-vue-next';
const inputMessage = ref('');
const textareaRef = ref<HTMLTextAreaElement | null>(null);

const props = defineProps<{
    loading: boolean;
    generating: boolean;
}>();

const emit = defineEmits<{
    (e: 'send-message', message: string): void;
    (e: 'stop'): void;
}>();

const adjustTextareaHeight = () => {
    if (textareaRef.value) {
        textareaRef.value.style.height = 'auto';
        textareaRef.value.style.height = `${textareaRef.value.scrollHeight}px`;
    }
};

function handleClick() {
    if (props.loading && props.generating) {
        emit('stop');
        console.log('Sending stop command');
        return;
    } else if (!props.loading && !props.generating && inputMessage.value.trim() !== '') {
        emit('send-message', inputMessage.value);
        console.log('Sending message:', inputMessage.value);
        inputMessage.value = '';
        nextTick(() => {
            adjustTextareaHeight();
        });
    }
};
</script>

<template>
    <div class="wrapper">
        <div class="chat-input">
            <textarea
                ref="textareaRef"
                v-model="inputMessage"
                @input="adjustTextareaHeight"
                @keydown.enter.exact.prevent="handleClick"
                placeholder="Type your message..."
                rows="1"
            />
            <button @click="handleClick" :disabled="loading && !generating">
                <ArrowUp class="send" v-if="!loading && !generating" />
                <LoaderCircle class="loader" v-else-if="!generating" />
                <Square class="stop" v-else />
            </button>
        </div>
    </div>
</template>

<style scoped>
.wrapper {
    padding: 1rem;
}

.chat-input {
    flex: 1;
    display: flex;
    align-items: flex-end;
    padding: 4px;
    border-radius: 1.5rem;
    background-color: var(--color-border);
}

textarea {
    flex: 1;
    padding: 0.5rem;
    font-size: 1rem;
    background-color: transparent;
    border: none;
    color: var(--color-text-strong);
    padding-left: 1rem;
    resize: none;
    overflow-y: hidden;
    min-height: 2.5rem;
    max-height: 200px;
    font-family: inherit;
    line-height: 1.5;
}

textarea:focus {
    outline: none;
}

textarea::-webkit-scrollbar {
    width: 8px;
}

textarea::-webkit-scrollbar-thumb {
    background-color: var(--color-background-mute);
    border-radius: 4px;
}

button {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 2.5rem;
    height: 2.5rem;
    min-width: 2.5rem;
    min-height: 2.5rem;
    border-radius: 50%;
    margin-bottom: 0;
}

.loader {
    animation: spin 1s linear infinite;
}

@keyframes spin {
    from {
        transform: rotate(0deg);
    }
    to {
        transform: rotate(360deg);
    }
}

.stop {
    fill: var(--color-background);
}
</style>