<script lang="ts">
	import { onMount } from "svelte";
	import { getAsync } from "./utils/http.util"
	import { getDateSeed } from "./utils/date.util";
    import { starles, names } from "./stores/game.store";
	import Game from "./components/Game.svelte";
	import type { Starle } from "./types/starle.type";
	import { fade } from "svelte/transition";

	let isLoading: boolean = true;

	onMount(async () => {
		// todo: save data to localStorage and prevent multiple api calls
		try {
			let starles_data = await getAsync<Starle[]>(`/api/starle?seed=${getDateSeed()}`);
			$starles = starles_data;

			let names_data = await getAsync<string[]>('/api/names');
			$names = names_data;
		} catch (error) {
            console.error('Error loading data:', error);
            // Handle error appropriately
        } finally {
            isLoading = false; // Set loading to false when data is loaded or in case of error
        }
	});
</script>

<main>
	{#if isLoading}
		<div class="loading-screen" in:fade={{ duration: 500 }}>
			Loading...
		</div>
	{:else}
		<div class="game-container" in:fade={{ duration: 500 }}>
			<Game />
		</div>
	{/if}
</main>

<style>
	.loading-screen {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
        font-size: 2em;
    }
</style>
