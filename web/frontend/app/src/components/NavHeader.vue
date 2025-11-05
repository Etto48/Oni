<template>
    <header>
        <img class="logo" src="@/assets/icon.svg" alt="Oni Logo" width="32" height="32" />
        <h1 class="gradient-text">Oni</h1>
    </header>
</template>

<style scoped>
header {
    display: flex;
    position: sticky;
    top: 0;
    left: 0;
    right: 0;
    width: 100vw;
    padding: 1rem;
    align-items: center;
    gap: 0.5rem;
}
h1 {
    font-weight: 900;
}
</style>