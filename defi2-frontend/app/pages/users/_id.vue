<template>
    <div class="flex flex-row">
        <div>
            <img src="/no_ppl.webp" class="h-1" alt="">
        </div>
        <div>
            <h1>Utilisateur {{ $route.params.id }}</h1>
            <p>Émission de CO2 évité : {{ savedCO }}</p>
        </div>
    </div>
</template>
<script setup lang="ts">

const savedCO = 10;
</script>