<script lang="ts">
    import type { Starle } from "../types/starle.type";
    import { starles, names } from "../stores/game.store"; 

    import { faPaperPlane } from '@fortawesome/free-solid-svg-icons';
    import Fa from "./Fa.svelte";
    
    let starle: Starle | undefined;

    $: if ($starles.length > 0) {
        starle = $starles.shift();
    }

    let searchTerm: string = "";
    let suggestions: string[] = [];

    // Reactive statement to update suggestions
    $: if (searchTerm.trim() !== '') {
        suggestions = $names.filter(name => 
            name.toLowerCase().includes(searchTerm.toLowerCase())
        );
    } else {
        suggestions = [];
    }

    /**
     * Trigger the handleSubmit function on `enter`
     * @param event
     */
    const handleKeydown = (event: KeyboardEvent): void => {
        if (event.key === 'Enter' && !event.shiftKey) { // Check for Enter key without Shift
            event.preventDefault(); // Prevent the default action (enter = new line)
            handleSubmit();
        }
    };

    /**
     * Handles the submit button click.
     */
    const handleSubmit = (): void => {
        if (searchTerm.toUpperCase() == starle?.name.toUpperCase()) {
            alert("Correct!");
            starle = $starles.shift();
            searchTerm = "";
        } else {
            alert("Wrong.");
        }
    }
</script>

<div class="game">
    <div>
        {#if starle && starle.movies}
            {#each starle.movies as movie (movie.title)}
                <div>
                    <p>{movie.title} <i>({movie.release_year})</i></p>
                </div>
            {/each}
        {/if}
    </div>
    <div class="searchbar">
        <textarea bind:value={searchTerm} on:keydown={handleKeydown} placeholder="Search for an actor..."/>
        <button on:click={handleSubmit} type="button" title="Send">
            <Fa icon={faPaperPlane} color='#89b4fa' />
        </button>
        {#if suggestions.length > 0}
            <ul>
                {#each suggestions as suggestion}
                    <li>{suggestion}</li>
                {/each}
            </ul>
        {/if}
    </div>
</div>

<style>
    .game {
        display: flex;
        flex-direction: column;
        row-gap: 34px;  
    }

    .searchbar {
        position: relative;
        bottom: 21px;
        display: flex;
        align-items: center;
        border-radius: 21px; /* Rounded borders at the top */
        padding: 6px 16px;
        box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.3); /* Optional: adds shadow for elevation effect */
        z-index: 100; /* Ensure it's above other elements */
        width: 100%;
        max-width: 680px; /* Adjust based on your design preference */
        margin: 0 auto; /* Center the searchbar container if it has a max-width */
        box-sizing: border-box;
    }

    textarea {
        flex-grow: 1;
        background-color: transparent;
        border: none;
        color: #cdd6f4; /* Light text color for visibility */
        margin-right: 8px;
        font-size: 16px;
        line-height: 2;
        resize: none; /* Disable resizing */
        outline: none; /* Disable outline */
        height: 32px;
    }

    button {
        border: none;
        background-color: transparent; 
        cursor: pointer;
        outline: none;
    }

    ul {
        list-style-type: none;
        padding: 0;
        margin: 0;
        border: 1px solid #ccc;
        border-top: none; /* Remove top border to blend with the input */
        border-radius: 0 0 4px 4px;
        max-height: 200px;
        overflow-y: auto; /* Enable scroll for long lists */
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    }

    li {
        padding: 10px;
        border-top: 1px solid #eee;
        cursor: pointer;
    }

    li:hover {
        background-color: #f5f5f5;
    }
</style>