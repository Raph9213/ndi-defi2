export const useAuthUI = () => {
    const panelMode = useState<string | null>('auth-panel-mode', () => null);
    const openPanel = (mode: string) => { panelMode.value = mode; };
    const closePanel = () => { panelMode.value = null; };

    return {
        panelMode,
        openPanel,
        closePanel
    };
};
