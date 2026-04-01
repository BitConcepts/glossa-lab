# Patent References

This directory contains patents that form the conceptual foundation for Glossa Lab's text analysis and visualization capabilities.

## US 2024/0248922 A1 — System and Methods for Searching Text Utilizing Categorical Touch Inputs

- **Inventor:** Michael Merkur (Thornhill, CA)
- **Filed:** January 19, 2024
- **Published:** July 25, 2024
- **Application No.:** 18/417,918

### Key Concepts

**1. Hierarchical text decomposition (Stories → Slices → Blocks)**
A written work is organized into a navigable tree: volumes → stories → slices → blocks. Each level is filterable and searchable. This provides a structural framework for decomposing any corpus — including ancient inscriptions — into manageable, addressable units.

**2. Categorical semantic tagging (Clusters + Manual Tags)**
Text segments are tagged with semantic categories from a predefined taxonomy (Culture, Nations, Nature, Religion, NSFW, People, Spiritual). Multiple clusters can be combined to filter text. Users can also apply manual tags. This enables concept-based navigation of a corpus.

**3. Phonetic color-coding system (Kandles)**
An extended Soundex-derived system that maps consonant sound groups to 7 colors:

| Number | Sound Groups | Color  | Nature Element |
|--------|-------------|--------|----------------|
| 1      | K, G, J, Ch | Yellow | Sun            |
| 2      | M, N        | Grey   | Moon           |
| 3      | T, D, Th    | Red    | Fire           |
| 4      | R, L        | Blue   | Water          |
| 5      | Y, W, H, Kh | Green | Tree           |
| 6      | P, B, F, V  | Purple | Flower         |
| 7      | S, Z, Sh    | Brown  | Soil           |

Words are color-coded based on the phonetic sound at the beginning of the word. This creates a visual representation of the phonetic structure of text.

**4. Color-coded grids**
Text is displayed as a grid where each cell is colored according to the Kandles system. The grid has equal rows and columns. This visual matrix creates a "phonetic fingerprint" of any text passage — making patterns visible that are invisible in raw text.

**5. Cross-language phonetic mapping**
The Kandles system maps to Japanese kanji elements (日=Sun, 月=Moon, 火=Fire, 水=Water, 木=Tree, 花=Flower, 土=Soil), suggesting a universal phonetic-to-visual mapping that transcends individual writing systems.

### Relevance to Glossa Lab

These concepts directly extend Glossa Lab's analytical capabilities:

- **Hierarchical decomposition** → structuring Indus inscriptions into addressable units
- **Semantic clustering** → concept-based exploration of ancient texts
- **Kandles color-coding** → visual phonetic fingerprinting of symbol sequences
- **Color grids** → revealing structural patterns across languages/scripts
- **Cross-language mapping** → comparing phonetic structures across writing systems

## 1394.003US — Formal Drawings

Companion formal drawing set for the patent above, including additional visual representations of:

- Color-coded text grids for song lyrics (word → color → number encoding)
- Grid templates with phonetic color-number mappings
- Visual fingerprint matrices

## Integration with Existing Analysis

The patented techniques **complement** (not replace) the statistical entropy analysis:

| Analysis Layer | Technique | What It Reveals |
|---------------|-----------|-----------------|
| Statistical | Block entropy (Rao et al.) | Whether a system is linguistic |
| Statistical | Zipf analysis | Frequency distribution structure |
| Structural | Hierarchical decomposition (Merkur) | How text units relate |
| Visual | Kandles color-coding (Merkur) | Phonetic pattern fingerprints |
| Semantic | Cluster tagging (Merkur) | Conceptual organisation |

The entropy analysis answers "is it language?" The Merkur techniques answer "what does the language look like, and how is it structured?"
