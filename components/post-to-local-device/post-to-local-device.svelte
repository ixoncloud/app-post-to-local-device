<script lang="ts">
  import { onMount } from "svelte";

  import type {
    BackendComponentClient,
    ComponentContext,
  } from "@ixon-cdk/types";

  export let context: ComponentContext;

  let rootEl: HTMLDivElement;

  let cloudFunctionsClient: BackendComponentClient;

  let httpServerName: string;
  let plcCommand: string;
  let action: string;
  let label: string;
  let baseValue: string;

  let disabled = false;

  onMount(() => {
    if (context.mode === "edit") {
      disabled = true;
    }

    httpServerName = context.inputs.httpServerName;
    plcCommand = context.inputs.plcCommand;
    action = context.inputs.action;
    label = context.inputs.label;
    baseValue = context.inputs.baseValue;

    cloudFunctionsClient = context.createBackendComponentClient();

    return () => {
      if (cloudFunctionsClient) {
        cloudFunctionsClient.destroy();
      }
    };
  });

  async function execute(value: string) {
    disabled = true;
    const response = await cloudFunctionsClient.call("execute", {
      httpServerName,
      plcCommand,
      value,
    });
    disabled = false;
    console.log(response);
  }
</script>

<div
  class="card flex justify-center {disabled ? 'pointer-events-none' : ''} "
  bind:this={rootEl}
>
  <div class="flex row p-4 justify-center">
    {#if !action || !label || !httpServerName || !plcCommand}
      <p>check inputs</p>
    {:else if action === "button"}
      <button
        class="button primary width-full"
        {disabled}
        on:click={() => execute(baseValue)}>{label}</button
      >
    {:else if action === "input"}
      <input
        type="text"
        class="input"
        bind:value={baseValue}
        {disabled}
      />
      <button
        class="button primary width-half max-width-200"
        {disabled}
        on:click={() => execute(baseValue)}>{label}</button
      >
    {/if}
  </div>
</div>

<style lang="scss">
  @import './styles/card';
  @import './styles/button';

  .pointer-events-none {
    pointer-events: none;
  }

  .input {
    width: 100%;
    margin-right: 8px;
  }

  .button {
    min-width: 16px;
    padding: 0 4px;
    overflow: hidden;
  }

  .width-half {
    width: 50%;
  }

  .max-width-200 {
    max-width: 200px;
  }

  .width-full {
    width: 100%;
  }

  .p-4 {
    padding: 4px;
  }

  .flex {
    display: flex;
  }

  .row {
    flex-direction: row;
  }

  .justify-center {
    justify-content: center;
  }
</style>
