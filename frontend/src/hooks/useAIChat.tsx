/**
 * Global AI chat context — allows any component to open the chat window
 * with pre-filled context and an initial prompt.
 *
 * Usage:
 *   const { openChat } = useAIChat();
 *   openChat({
 *     contextType: "study",
 *     contextId: study.id,
 *     contextLabel: study.name,
 *     initialPrompt: "Help me design experiments for this study about...",
 *   });
 */
import { createContext, useCallback, useContext, useState } from "react";

export interface ChatRequest {
  contextType?: "corpus" | "experiment" | "study" | "";
  contextId?: string;
  contextLabel?: string;
  initialPrompt?: string;
}

interface AIChatCtx {
  isOpen: boolean;
  request: ChatRequest | null;
  openChat: (req?: ChatRequest) => void;
  closeChat: () => void;
  toggleChat: () => void;
  isDocked: boolean;
  setDocked: (v: boolean) => void;
}

const AIChatContext = createContext<AIChatCtx>({
  isOpen: false,
  request: null,
  openChat: () => {},
  closeChat: () => {},
  toggleChat: () => {},
  isDocked: false,
  setDocked: () => {},
});

export function AIChatProvider({ children }: { children: React.ReactNode }) {
  const [isOpen, setIsOpen] = useState(false);
  const [request, setRequest] = useState<ChatRequest | null>(null);
  const [isDocked, setDocked] = useState(false);

  const openChat = useCallback((req?: ChatRequest) => {
    if (req) setRequest(req);
    setIsOpen(true);
    // Always route through the docked side panel — the floating chat window
    // has been retired. App-level handler listens for this event.
    window.dispatchEvent(new CustomEvent("glossa:open-ai-panel"));
  }, []);

  const closeChat = useCallback(() => setIsOpen(false), []);

  const toggleChat = useCallback(() => {
    setIsOpen((v) => !v);
    if (!isOpen) setRequest(null);
  }, [isOpen]);

  return (
    <AIChatContext.Provider value={{ isOpen, request, openChat, closeChat, toggleChat, isDocked, setDocked }}>
      {children}
    </AIChatContext.Provider>
  );
}

export function useAIChat(): AIChatCtx {
  return useContext(AIChatContext);
}
