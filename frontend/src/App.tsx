import {
  AlertCircle,
  CheckCircle2,
  ImagePlus,
  LoaderCircle,
  RefreshCw,
  Shirt,
  Upload,
} from "lucide-react";
import type { ChangeEvent } from "react";
import { useCallback, useEffect, useMemo, useState } from "react";

type ClothingAttributes = {
  category: string;
  colors: string[];
  seasons: string[];
  style_tags: string[];
  description: string;
};

type ClothingItem = {
  id: string;
  original_filename: string;
  image_url: string;
  attributes: ClothingAttributes;
  created_at: string;
};

type RegisterItemResponse = {
  item: ClothingItem;
  vector_status: string;
};

type ItemsState =
  | { status: "loading"; items?: undefined; error?: undefined }
  | { status: "success"; items: ClothingItem[]; error?: undefined }
  | { status: "error"; items?: undefined; error: string };

type UploadState =
  | { status: "idle"; message?: undefined }
  | { status: "uploading"; message?: undefined }
  | { status: "success"; message: string }
  | { status: "error"; message: string };

const apiBaseUrl = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";
const imageInputId = "wardrobe-image-input";

export function App() {
  const [itemsState, setItemsState] = useState<ItemsState>({ status: "loading" });
  const [uploadState, setUploadState] = useState<UploadState>({ status: "idle" });
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);

  const items = itemsState.status === "success" ? itemsState.items : [];
  const itemCountLabel = useMemo(() => `${items.length} items`, [items.length]);

  const fetchItems = useCallback(async () => {
    setItemsState({ status: "loading" });

    try {
      const response = await fetch(`${apiBaseUrl}/api/items`);

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }

      setItemsState({
        status: "success",
        items: (await response.json()) as ClothingItem[],
      });
    } catch (error) {
      const message = error instanceof Error ? error.message : "Unknown error";
      setItemsState({ status: "error", error: message });
    }
  }, []);

  useEffect(() => {
    void fetchItems();
  }, [fetchItems]);

  useEffect(() => {
    if (!selectedFile) {
      setPreviewUrl(null);
      return undefined;
    }

    const objectUrl = URL.createObjectURL(selectedFile);
    setPreviewUrl(objectUrl);
    return () => URL.revokeObjectURL(objectUrl);
  }, [selectedFile]);

  const onSelectFile = (event: ChangeEvent<HTMLInputElement>) => {
    setUploadState({ status: "idle" });
    setSelectedFile(event.target.files?.[0] ?? null);
    event.currentTarget.value = "";
  };

  const registerItem = useCallback(async () => {
    if (!selectedFile) {
      return;
    }

    setUploadState({ status: "uploading" });

    try {
      const response = await fetch(`${apiBaseUrl}/api/items`, {
        method: "POST",
        headers: {
          "Content-Type": selectedFile.type || "application/octet-stream",
          "X-Wardrobe-Filename": encodeURIComponent(selectedFile.name),
        },
        body: selectedFile,
      });

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }

      const result = (await response.json()) as RegisterItemResponse;
      setUploadState({
        status: "success",
        message: `${result.item.original_filename} / ${result.vector_status}`,
      });
      setSelectedFile(null);
      await fetchItems();
    } catch (error) {
      const message = error instanceof Error ? error.message : "Unknown error";
      setUploadState({ status: "error", message });
    }
  }, [fetchItems, selectedFile]);

  const isUploading = uploadState.status === "uploading";

  return (
    <main className="app-shell">
      <section className="workspace" aria-labelledby="app-title">
        <header className="topbar">
          <div className="brand">
            <span className="brand-icon" aria-hidden="true">
              <Shirt size={22} strokeWidth={2.1} />
            </span>
            <div>
              <h1 id="app-title">Wardrobe</h1>
              <p>Item registration</p>
            </div>
          </div>
          <div className="topbar-actions">
            <span className="status-pill">
              <CheckCircle2 size={16} />
              {itemCountLabel}
            </span>
            <button
              type="button"
              className="icon-button"
              onClick={() => void fetchItems()}
              aria-label="Refresh items"
              title="Refresh items"
            >
              <RefreshCw size={17} />
            </button>
          </div>
        </header>

        <div className="inventory-layout">
          <section className="upload-panel" aria-labelledby="upload-title">
            <div className="panel-heading">
              <ImagePlus size={20} />
              <h2 id="upload-title">Register item</h2>
            </div>

            <div className="drop-zone">
              {previewUrl ? (
                <img src={previewUrl} alt="" />
              ) : (
                <div className="drop-zone-empty" aria-hidden="true">
                  <ImagePlus size={34} />
                </div>
              )}
            </div>

            <div className="upload-controls">
              <input
                id={imageInputId}
                type="file"
                accept="image/png,image/jpeg,image/webp"
                onChange={onSelectFile}
              />
              <label className="secondary-button" htmlFor={imageInputId}>
                <ImagePlus size={16} />
                Select image
              </label>
              <button
                type="button"
                onClick={() => void registerItem()}
                disabled={!selectedFile || isUploading}
              >
                {isUploading ? <LoaderCircle size={16} className="spin" /> : <Upload size={16} />}
                Register
              </button>
            </div>

            <div className={`upload-status upload-status-${uploadState.status}`}>
              {uploadState.status === "idle" && (selectedFile?.name ?? "No image selected")}
              {uploadState.status === "uploading" && "Uploading"}
              {uploadState.status === "success" && uploadState.message}
              {uploadState.status === "error" && uploadState.message}
            </div>
          </section>

          <section className="inventory-panel" aria-labelledby="inventory-title">
            <div className="panel-heading inventory-heading">
              <Shirt size={20} />
              <h2 id="inventory-title">Items</h2>
            </div>

            {itemsState.status === "loading" && (
              <div className="feedback">
                <LoaderCircle size={18} className="spin" />
                Loading
              </div>
            )}

            {itemsState.status === "error" && (
              <div className="feedback feedback-error">
                <AlertCircle size={18} />
                {itemsState.error}
              </div>
            )}

            {itemsState.status === "success" && items.length === 0 && (
              <div className="empty-state">
                <Shirt size={30} />
                Empty wardrobe
              </div>
            )}

            {items.length > 0 && (
              <div className="item-grid">
                {items.map((item) => (
                  <article className="item-card" key={item.id}>
                    <img
                      src={`${apiBaseUrl}${item.image_url}`}
                      alt={item.original_filename}
                      loading="lazy"
                    />
                    <div className="item-body">
                      <div>
                        <h3>{item.attributes.category}</h3>
                        <p>{formatDate(item.created_at)}</p>
                      </div>
                      <div className="tag-row" aria-label="colors">
                        {item.attributes.colors.map((color) => (
                          <span className="tag color-tag" key={color}>
                            {color}
                          </span>
                        ))}
                      </div>
                      <div className="tag-row" aria-label="style tags">
                        {[...item.attributes.seasons, ...item.attributes.style_tags].map((tag) => (
                          <span className="tag" key={tag}>
                            {tag}
                          </span>
                        ))}
                      </div>
                      <p className="item-description">{item.attributes.description}</p>
                    </div>
                  </article>
                ))}
              </div>
            )}
          </section>
        </div>
      </section>
    </main>
  );
}

function formatDate(value: string) {
  return new Intl.DateTimeFormat("ja-JP", {
    dateStyle: "medium",
    timeStyle: "short",
  }).format(new Date(value));
}
