<script lang="ts">
  import { onMount } from 'svelte';

  import type { BackendComponentClient, ComponentContext } from '@ixon-cdk/types';

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
    if (context.mode === 'edit') {
      disabled = true;
    }

    label = context.inputs.info?.label || context.inputs.label;
    action = context.inputs.info?.action || context.inputs.action;
    httpServerName =
      context.inputs.settings?.httpServerName || context.inputs.httpServerName;
    plcCommand =
      context.inputs.settings?.plcCommand || context.inputs.plcCommand;
    baseValue = context.inputs.settings?.baseValue || context.inputs.baseValue;

    cloudFunctionsClient = context.createBackendComponentClient();

    return () => {
      if (cloudFunctionsClient) {
        cloudFunctionsClient.destroy();
      }
    };
  });

  async function execute(value: string) {
    disabled = true;
    const response = await cloudFunctionsClient.call('execute', {
      httpServerName,
      plcCommand,
      value,
    });
    disabled = false;
  }
</script>

<div
  class="card flex justify-center {disabled ? 'pointer-events-none' : ''} "
  bind:this={rootEl}
>
  <div class="flex row p-4 justify-center">
    {#if !action || !label || !httpServerName || !plcCommand}
      <p>check inputs</p>
    {:else if action === 'button'}
      <button
        class="button primary width-full"
        {disabled}
        on:click={() => execute(baseValue)}>{label}</button
      >
    {:else if action === 'input'}
      <input type="text" class="input" bind:value={baseValue} {disabled} />
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
