# Component properties

Use this reference to configure the 15 samples without opening an external guide. Each property links to its YAML declaration.

Generated from the current source. Descriptions express the source contract; Power Apps Studio import and runtime behavior remain unverified.

An **input** supplies a value. An **output** exposes a value. An **event** calls a host-app formula. An **action** lets the host call component behavior. Function properties accept parameters and return values.

Set properties on a component instance in Studio. Replace instance names in formulas with your own names.

Start with [shared settings](THEMING.md). The original 12 components use `AccentColor`, `Motion`, and supported individual inputs. The three new components use `Design = UiTheme`.

Keep existing Studio identifiers when updating an app. Changing a public identifier can break existing formulas.

Long table and record defaults link to their complete source formulas, including sample field names. An em dash means no custom default is declared.

## Index

- [Accordion](#accordion)
- [Attachments list with upload](#attachments-list)
- [Button](#button)
- [Carousel](#carousel)
- [Data table](#data-table)
- [Floating action button](#floating-action-button)
- [Form field](#form-field)
- [Kanban board](#kanban-board)
- [KPI card](#kpi-card)
- [Message banner](#message-banner)
- [Month calendar](#month-calendar)
- [Navigation shell](#navigation-shell)
- [Search and filter bar](#search-filter-bar)
- [Stepper](#stepper)
- [Tree view](#tree-view)

<a id="accordion"></a>

## Accordion

**Studio name:** `lcsAccordion` · [Setup guide](../accordion/README.md) · [Source](../accordion/component.yaml)

| Property | Kind | Type / parameters | Default | Purpose |
| --- | --- | --- | --- | --- |
| [Items](../accordion/component.yaml#L6) | Input | Table | [Source formula](../accordion/component.yaml#L6) | The sections, as a table with Key, Title and Body columns, such as Table({Key: "hours", Title: "Opening hours", Body: "Weekdays 8 to 6."}). |
| [MultipleOpen](../accordion/component.yaml#L13) | Input | Boolean | <code>=false</code> | Lets several sections be open at once. Off, opening one closes the others. |
| [DefaultOpenKeys](../accordion/component.yaml#L19) | Input | Text | <code>=""</code> | The sections open when the screen loads, by Key, separated by commas. |
| [BodySize](../accordion/component.yaml#L25) | Input | Number | <code>=14</code> | The text size of a section's body. |
| [AccentColor](../accordion/component.yaml#L31) | Input | Color | <code>=ColorValue("#463782")</code> | Your brand colour, for the open section's chevron circle and the focus ring. |
| [Theme](../accordion/component.yaml#L37) | Input | Text | <code>="Light"</code> | Light, or Dark for a dark screen. |
| [Motion](../accordion/component.yaml#L43) | Input | Boolean | <code>=true</code> | The chevron's circle pops in as a section opens. None plays for people who've asked their device for reduced motion. |
| [OpenKeys](../accordion/component.yaml#L49) | Output | Text | — | The open sections' keys, separated by commas; empty when all are closed. |
| [OpenCount](../accordion/component.yaml#L54) | Output | Number | — | How many sections are open. |
| [OnToggle](../accordion/component.yaml#L59) | Event | (Key: Text, IsOpen: Boolean) → None | <code>=false</code> | Runs in your app when a section opens or closes, with its key and whether it's open now. |
| [Toggle](../accordion/component.yaml#L74) | Action | (Key: Text) → None | — | Opens a section, or closes it if it's open, by Key, such as from a link elsewhere on the screen. |
| [ExpandAll](../accordion/component.yaml#L84) | Action | None | — | Opens every section. With MultipleOpen off, opens the first. |
| [CollapseAll](../accordion/component.yaml#L89) | Action | None | — | Closes every section. |

<a id="attachments-list"></a>

## Attachments list with upload

**Studio name:** `lcsAttachmentList` · [Setup guide](../attachments-list/README.md) · [Source](../attachments-list/component.yaml)

| Property | Kind | Type / parameters | Default | Purpose |
| --- | --- | --- | --- | --- |
| [Title](../attachments-list/component.yaml#L7) | Input | Text | <code>="Upload documents"</code> | The heading at the top of the card. |
| [Subtitle](../attachments-list/component.yaml#L13) | Input | Text | <code>="Add the files for this request"</code> | A line under the heading. Empty shows none. |
| [Files](../attachments-list/component.yaml#L19) | Input | Table | [Source formula](../attachments-list/component.yaml#L19) | The files already attached, as a table with Key, Name, Size (bytes, 0 when unknown), Url (a link that opens the file, or empty), Who and When columns. |
| [AcceptedTypes](../attachments-list/component.yaml#L26) | Input | Text | <code>="pdf,docx,xlsx,png,jpg"</code> | The file types people can add, as extensions separated by commas, such as pdf,docx,xlsx. Shown as chips; another type is added with a reason and isn't uploaded. Empty accepts any type. |
| [MaxFiles](../attachments-list/component.yaml#L32) | Input | Number | <code>=3</code> | The most files people can add before they upload. Files already attached don't count. |
| [MaxFileSize](../attachments-list/component.yaml#L38) | Input | Number | <code>=10</code> | The largest file in megabytes (1 MB is 1,000,000 bytes). Power Apps' Attachments control refuses a bigger file with its own message. |
| [AllowUpload](../attachments-list/component.yaml#L44) | Input | Boolean | <code>=true</code> | Shows the drop card and the Upload button. Off, the card lists the files already attached. |
| [AllowRemove](../attachments-list/component.yaml#L50) | Input | Boolean | <code>=true</code> | Shows a remove button on each file already attached. Removing marks the file, with Undo, until the changes are saved. |
| [IsUploading](../attachments-list/component.yaml#L56) | Input | Boolean | <code>=false</code> | Set it to true while your app saves (in OnSave), and back to false after: each file shows a moving bar, the button spins, and nothing can be changed. |
| [ShowMeta](../attachments-list/component.yaml#L62) | Input | Text | <code>="size,who,when"</code> | Which details show under a file already attached: size, who, when, or any of them separated by commas. Empty shows none. |
| [OpenOnSelect](../attachments-list/component.yaml#L68) | Input | Boolean | <code>=true</code> | Opens an attached file's Url in a new tab when its row is selected, before OnOpen runs. Off, only OnOpen runs. |
| [EmptyText](../attachments-list/component.yaml#L74) | Input | Text | <code>="No files yet"</code> | What the card says when AllowUpload is off and nothing is attached. |
| [MaxHeight](../attachments-list/component.yaml#L80) | Input | Number | <code>=0</code> | The most height the files already attached take before they scroll. 0 grows with the list. |
| [AccentColor](../attachments-list/component.yaml#L86) | Input | Color | <code>=ColorValue("#463782")</code> | Your brand colour, for the drop card, the button, the focus rings and files of a type without a colour of its own. |
| [Theme](../attachments-list/component.yaml#L92) | Input | Text | <code>="Light"</code> | Light, or Dark for a dark screen. |
| [Motion](../attachments-list/component.yaml#L98) | Input | Boolean | <code>=true</code> | The arrow bobs when the card appears, tiles pop in, ticks draw in, and bars move while uploading. None plays for people who've asked their device for reduced motion. |
| [Count](../attachments-list/component.yaml#L104) | Output | Number | — | How many files are already attached. |
| [TotalSize](../attachments-list/component.yaml#L109) | Output | Number | — | The attached files' sizes added up, in bytes. |
| [TotalSizeText](../attachments-list/component.yaml#L114) | Output | Text | — | The total size as people read it, such as 1.8 MB. |
| [ReadyCount](../attachments-list/component.yaml#L119) | Output | Number | — | How many added files are ready to upload. |
| [StagedFiles](../attachments-list/component.yaml#L124) | Output | Table | — | The files ready to upload, with Name and Value as Power Apps' Attachments control gives them: for a SharePoint item's attachments or a Dataverse file column. |
| [StagedFilesData](../attachments-list/component.yaml#L129) | Output | Table | — | The files ready to upload as Name and ContentBytes (base64), for a flow that takes text. Built when the Upload button is selected, so read it in OnSave. |
| [RemovedKeys](../attachments-list/component.yaml#L134) | Output | Table | — | The Key of each attached file marked for removal, in a Key column. |
| [HasChanges](../attachments-list/component.yaml#L139) | Output | Boolean | — | True while there are files to upload or files to remove. |
| [OnOpen](../attachments-list/component.yaml#L144) | Event | (Key: Text, Name: Text, Url: Text) → None | <code>=false</code> | Runs in your app when an attached file's row or Open is selected, with its key, name and link. Open a file your own way here, such as through a flow. |
| [OnSave](../attachments-list/component.yaml#L163) | Event | (Ready: Number, Removed: Number) → None | <code>=false</code> | Runs in your app when Upload is selected, with how many files to upload and to remove. Save StagedFiles (or StagedFilesData for a flow) and remove RemovedKeys, with IsUploading true while you do, then Reset this component. |
| [OnCancel](../attachments-list/component.yaml#L178) | Event | (Discarded: Number) → None | <code>=false</code> | Runs in your app after Cancel has cleared the added files and the removals, with how many changes were dropped. |

<a id="button"></a>

## Button

**Studio name:** `lcsButton` · [Setup guide](../button/README.md) · [Source](../button/component.yaml)

| Property | Kind | Type / parameters | Default | Purpose |
| --- | --- | --- | --- | --- |
| [Label](../button/component.yaml#L6) | Input | Text | <code>="Save"</code> | The button's text. |
| [Appearance](../button/component.yaml#L12) | Input | Text | <code>="Primary"</code> | Primary, Secondary, Outline or Subtle. |
| [IconName](../button/component.yaml#L18) | Input | Text | <code>=""</code> | A Fluent icon name, such as Checkmark. Leave empty for no icon. |
| [Shape](../button/component.yaml#L24) | Input | Text | <code>="Pill"</code> | Pill or Rounded. Pill uses half the smaller dimension; unknown values also use Pill. |
| [CornerRadius](../button/component.yaml#L30) | Input | Number | <code>=12</code> | Corner radius in pixels for Rounded. Blank uses 12; values are clamped from zero to half the smaller dimension. Ignored for Pill. |
| [IsBusy](../button/component.yaml#L36) | Input | Boolean | <code>=false</code> | While true, the button is disabled and says it's working. |
| [AccentColor](../button/component.yaml#L42) | Input | Color | <code>=ColorValue("#463782")</code> | Your brand colour. Primary buttons use it, and their hover and pressed colours are worked out from it. |
| [Theme](../button/component.yaml#L48) | Input | Text | <code>="Light"</code> | Light, or Dark for a dark screen: text and borders turn light, Secondary is drawn as Outline and Subtle as Transparent. |
| [RequireConfirm](../button/component.yaml#L54) | Input | Boolean | <code>=false</code> | When true, the first select turns the button red and shows ConfirmLabel; OnClick runs only if it's selected again within ConfirmSeconds. |
| [ConfirmLabel](../button/component.yaml#L60) | Input | Text | <code>="Select again"</code> | What the button says while it waits for the confirming select. |
| [ConfirmSeconds](../button/component.yaml#L66) | Input | Number | <code>=4</code> | How long the button waits for the confirming select before it goes back to normal. |
| [Motion](../button/component.yaml#L72) | Input | Boolean | <code>=true</code> | When the button starts working (IsBusy), a soft shade sweeps across it once. None plays for people who've asked their device for reduced motion. |
| [IsArmed](../button/component.yaml#L78) | Output | Boolean | — | True while the button waits for the confirming select. |
| [ClickCount](../button/component.yaml#L83) | Output | Number | — | How many times the button was selected since the last ResetCount(). |
| [FormatLabel](../button/component.yaml#L88) | InputFunction | (Text: Text) → Text | <code>=Text</code> | Lets the app change how the label is shown. Receives the label, returns the text to show. |
| [IsValidLabel](../button/component.yaml#L99) | OutputFunction | (Text: Text) → Boolean | — | True when the text is a usable button label: not empty and at most 40 characters. |
| [OnClick](../button/component.yaml#L109) | Event | (Count: Number) → None | <code>=false</code> | Runs in the app when the button is selected. Receives the new click count. |
| [ResetCount](../button/component.yaml#L120) | Action | None | — | Sets ClickCount back to 0. |

<a id="carousel"></a>

## Carousel

**Studio name:** `lcsCarousel` · [Setup guide](../carousel/README.md) · [Source](../carousel/component.yaml)

| Property | Kind | Type / parameters | Default | Purpose |
| --- | --- | --- | --- | --- |
| [Items](../carousel/component.yaml#L6) | Input | Table | [Source formula](../carousel/component.yaml#L6) | The slides, as a table with Key, Title, Text, Image (a picture URL, or empty) and Color (a hex used behind the text when there's no picture) columns. |
| [AutoPlay](../carousel/component.yaml#L13) | Input | Boolean | <code>=true</code> | Advances the slides by itself. People can pause it; a screen reader user should be able to, so leave the pause control on. |
| [Interval](../carousel/component.yaml#L19) | Input | Number | <code>=5000</code> | How long each slide stays, in milliseconds, when AutoPlay is on. |
| [Loop](../carousel/component.yaml#L25) | Input | Boolean | <code>=true</code> | Goes back to the first slide after the last. Off, it stops at the last and the next arrow is disabled. |
| [ShowDots](../carousel/component.yaml#L31) | Input | Boolean | <code>=true</code> | Shows a dot per slide under the picture; each is a button to that slide. |
| [ShowArrows](../carousel/component.yaml#L37) | Input | Boolean | <code>=true</code> | Shows the previous and next arrows. |
| [ShowPause](../carousel/component.yaml#L43) | Input | Boolean | <code>=true</code> | Shows the pause and play control when AutoPlay is on. |
| [ShowCaptions](../carousel/component.yaml#L49) | Input | Boolean | <code>=true</code> | Shows each slide's title and text over its lower part. |
| [AccentColor](../carousel/component.yaml#L55) | Input | Color | <code>=ColorValue("#463782")</code> | Your brand colour, for the current dot and the focus rings. |
| [Theme](../carousel/component.yaml#L61) | Input | Text | <code>="Light"</code> | Light, or Dark for a dark screen. |
| [Motion](../carousel/component.yaml#L67) | Input | Boolean | <code>=true</code> | A slide fades in when it arrives. None plays for people who've asked their device for reduced motion; the slides still change. |
| [CurrentIndex](../carousel/component.yaml#L73) | Output | Number | — | The slide showing now, 1 for the first. |
| [CurrentKey](../carousel/component.yaml#L78) | Output | Text | — | The Key of the slide showing now. |
| [IsPlaying](../carousel/component.yaml#L83) | Output | Boolean | — | True while the slides advance by themselves. |
| [OnChange](../carousel/component.yaml#L88) | Event | (Key: Text, Index: Number) → None | <code>=false</code> | Runs in your app when the slide changes, by the timer or by a person. |
| [OnSelect](../carousel/component.yaml#L103) | Event | (Key: Text, Index: Number) → None | <code>=false</code> | Runs in your app when the slide itself is selected, to open what it's about. |
| [Next](../carousel/component.yaml#L118) | Action | None | — | Goes to the next slide, or the first after the last when Loop is on. |
| [Previous](../carousel/component.yaml#L123) | Action | None | — | Goes to the slide before, or the last from the first when Loop is on. |
| [GoTo](../carousel/component.yaml#L128) | Action | (Index: Number) → None | — | Goes to a slide by position, 1 for the first. |
| [Play](../carousel/component.yaml#L138) | Action | None | — | Starts advancing the slides by the timer. |
| [Pause](../carousel/component.yaml#L143) | Action | None | — | Stops the timer; the slides stay until a person moves them. |

<a id="data-table"></a>

## Data table

**Studio name:** `lcsDataTable` · [Setup guide](../data-table/README.md) · [Source](../data-table/component.yaml)

| Property | Kind | Type / parameters | Default | Purpose |
| --- | --- | --- | --- | --- |
| [Columns](../data-table/component.yaml#L6) | Input | Table | [Source formula](../data-table/component.yaml#L6) | The columns, in order, up to six: Label, Width in pixels, and Kind: Text, Strong (bold), Badge (a coloured pill) or Progress (a segmented bar from text such as 2/4). Column 1 shows C1 from Rows, and so on. |
| [Rows](../data-table/component.yaml#L20) | Input | Table | [Source formula](../data-table/component.yaml#L20) | The rows: Id, and the text for each column in C1 to C6. Sort, filter and page them in your app. |
| [BadgeStyles](../data-table/component.yaml#L32) | Input | Table | [Source formula](../data-table/component.yaml#L32) | The colours of Badge pills by their text: Value, Fill and Ink. Text with no style is grey. |
| [View](../data-table/component.yaml#L47) | Input | Text | <code>="Table"</code> | The view to start with: Table, Cards or List. |
| [ShowViewToggle](../data-table/component.yaml#L53) | Input | Boolean | <code>=true</code> | Shows the Table, Cards and List switch. |
| [TitleColumn](../data-table/component.yaml#L59) | Input | Number | <code>=2</code> | The column that names a row: the title of a card or list item, and the name screen readers hear. |
| [SubtitleColumn](../data-table/component.yaml#L65) | Input | Number | <code>=1</code> | The column shown small above a card's title and under a list item's. |
| [Sortable](../data-table/component.yaml#L71) | Input | Boolean | <code>=true</code> | Column headers can be selected to sort. The table runs OnSort; your app sorts Rows. |
| [Selectable](../data-table/component.yaml#L77) | Input | Boolean | <code>=true</code> | Shows a checkbox on each row, and one to select them all in table view. |
| [BulkActions](../data-table/component.yaml#L83) | Input | Text | <code>=""</code> | Buttons for the selected rows, separated by commas, such as Approve,Reject. Up to three. Leave empty for none. |
| [RowActions](../data-table/component.yaml#L89) | Input | Text | <code>="View,Edit,Delete"</code> | The row menu, separated by commas, such as View,Edit,Delete. Up to three. Leave empty for no menu. |
| [Density](../data-table/component.yaml#L95) | Input | Text | <code>="Comfortable"</code> | Comfortable (60 tall rows, easy to touch) or Compact (44). |
| [Loading](../data-table/component.yaml#L101) | Input | Boolean | <code>=false</code> | Shows grey placeholder rows while your app loads the data. |
| [EmptyTitle](../data-table/component.yaml#L107) | Input | Text | <code>="No items found"</code> | The heading when there are no rows. |
| [EmptyText](../data-table/component.yaml#L113) | Input | Text | <code>="Try changing your search or filters."</code> | The line under it. |
| [AccentColor](../data-table/component.yaml#L119) | Input | Color | <code>=ColorValue("#463782")</code> | Your brand colour, for progress, checkboxes and the selected rows. |
| [Theme](../data-table/component.yaml#L125) | Input | Text | <code>="Light"</code> | Light, or Dark for a dark screen. |
| [Motion](../data-table/component.yaml#L131) | Input | Boolean | <code>=true</code> | Plays short animations: progress segments fill in one after another, a highlight sweeps once across the loading rows, and the empty state's icon pops in. None plays for people who've asked their device for reduced motion. |
| [CurrentView](../data-table/component.yaml#L137) | Output | Text | — | The view shown now: Table, Cards or List. |
| [SortColumn](../data-table/component.yaml#L142) | Output | Number | — | The column sorted by, from 1; 0 for none. |
| [SortDescending](../data-table/component.yaml#L147) | Output | Boolean | — | True when the sort runs from Z to A or high to low. |
| [SelectedIds](../data-table/component.yaml#L152) | Output | Text | — | The selected rows' Ids, separated by semicolons. |
| [SelectedCount](../data-table/component.yaml#L157) | Output | Number | — | How many rows are selected, including any no longer in Rows. |
| [SelectedRows](../data-table/component.yaml#L162) | Output | Table | — | The selected rows that are in Rows now. |
| [OnRowSelect](../data-table/component.yaml#L167) | Event | (RowId: Text) → None | <code>=false</code> | Runs in your app when the user selects a row, a card or a list item, such as to open it. |
| [OnRowAction](../data-table/component.yaml#L178) | Event | (Action: Text, RowId: Text) → None | <code>=false</code> | Runs in your app when the user chooses from a row's menu. |
| [OnBulkAction](../data-table/component.yaml#L193) | Event | (Action: Text, RowIds: Text) → None | <code>=false</code> | Runs in your app when the user selects a button for the selected rows. |
| [OnSort](../data-table/component.yaml#L208) | Event | (ColumnNumber: Number, Descending: Boolean) → None | <code>=false</code> | Runs in your app when the user selects a column header. Sort Rows by that column. |
| [OnViewChange](../data-table/component.yaml#L223) | Event | (NewView: Text) → None | <code>=false</code> | Runs in your app when the user switches between Table, Cards and List. |
| [ClearSelection](../data-table/component.yaml#L234) | Action | None | — | Clears every checkbox, such as after a bulk action. |

<a id="floating-action-button"></a>

## Floating action button

**Studio name:** `lcsFab` · [Setup guide](../floating-action-button/README.md) · [Source](../floating-action-button/component.yaml)

| Property | Kind | Type / parameters | Default | Purpose |
| --- | --- | --- | --- | --- |
| [Icon](../floating-action-button/component.yaml#L6) | Input | Text | <code>="Add"</code> | The icon: Add, Edit, Send, Search, Upload, Download, Camera, Check, Share, Chat or Close. |
| [Label](../floating-action-button/component.yaml#L12) | Input | Text | <code>="Add new"</code> | What the button does, such as Add new or New request. Shown when Extended is true, and always read by screen readers. |
| [Extended](../floating-action-button/component.yaml#L18) | Input | Boolean | <code>=false</code> | When true, the button shows its label next to the icon. |
| [Size](../floating-action-button/component.yaml#L24) | Input | Text | <code>="Regular"</code> | Small (40), Regular (56) or Large (72). |
| [AccentColor](../floating-action-button/component.yaml#L30) | Input | Color | <code>=ColorValue("#463782")</code> | The button's colour. Use your app's brand colour. |
| [ContentColor](../floating-action-button/component.yaml#L36) | Input | Color | <code>=RGBA(255, 255, 255, 1)</code> | The icon and label colour on the button. Keep it readable on AccentColor. |
| [SpeedDial](../floating-action-button/component.yaml#L42) | Input | Boolean | <code>=false</code> | When true, the button opens a menu of Items instead of running OnSelect. |
| [Items](../floating-action-button/component.yaml#L48) | Input | Table | [Source formula](../floating-action-button/component.yaml#L48) | The speed-dial actions, as a table with Key, Icon and Label columns. Key is a short id your OnItemSelect checks, such as note. Three to six work best. |
| [HiddenKeys](../floating-action-button/component.yaml#L59) | Input | Text | <code>=""</code> | Keys of items to hide, separated by commas, such as If(!IsAdmin, "delete", ""). Empty shows every item. |
| [DisabledKeys](../floating-action-button/component.yaml#L65) | Input | Text | <code>=""</code> | Keys of items to show greyed out and unselectable, separated by commas. |
| [Direction](../floating-action-button/component.yaml#L71) | Input | Text | <code>="Up"</code> | Where the menu opens: Up (above the button, for the bottom of a screen) or Down (below it, for the top). |
| [ItemHeight](../floating-action-button/component.yaml#L77) | Input | Number | <code>=48</code> | The height of each speed-dial row in pixels. 44 or more is easy to tap. |
| [Disabled](../floating-action-button/component.yaml#L83) | Input | Boolean | <code>=false</code> | When true, the button is greyed out and can't be selected. |
| [Motion](../floating-action-button/component.yaml#L89) | Input | Boolean | <code>=true</code> | With a speed dial, its icon turns into the close mark as the menu opens, and back as it closes, and the menu's icons pop in. None plays for people who've asked their device for reduced motion. |
| [IsOpen](../floating-action-button/component.yaml#L95) | Output | Boolean | — | True while the speed-dial menu is open. |
| [SelectedKey](../floating-action-button/component.yaml#L100) | Output | Text | — | The Key of the speed-dial item chosen last. |
| [IconSvg](../floating-action-button/component.yaml#L105) | OutputFunction | (Name: Text, Stroke: Text) → Text | — | Returns one of the button's icons as an image your app can use, in any colour: set an Image control's Image to it. |
| [OnSelect](../floating-action-button/component.yaml#L119) | Event | None | <code>=false</code> | Runs in the app when the button is selected and SpeedDial is false. |
| [OnItemSelect](../floating-action-button/component.yaml#L125) | Event | (Key: Text, Label: Text) → None | <code>=false</code> | Runs in the app when a speed-dial item is selected. Receives its Key and Label; use Switch(Key, ...) for what each does. The menu has already closed. |
| [Open](../floating-action-button/component.yaml#L140) | Action | None | — | Opens the speed-dial menu. |
| [Close](../floating-action-button/component.yaml#L145) | Action | None | — | Closes the speed-dial menu. |
| [Toggle](../floating-action-button/component.yaml#L150) | Action | None | — | Opens the speed-dial menu if it's closed, and closes it if it's open. |

<a id="form-field"></a>

## Form field

**Studio name:** `uiFormField` · [Setup guide](../form-field/README.md) · [Source](../form-field/component.yaml)

| Property | Kind | Type / parameters | Default | Purpose |
| --- | --- | --- | --- | --- |
| [Label](../form-field/component.yaml#L7) | Input | Text | <code>="Project name"</code> | Visible field name. Supply a meaningful, nonblank label. |
| [DefaultText](../form-field/component.yaml#L13) | Input | Text | <code>=""</code> | Initial text and the value restored by Reset(componentInstance). |
| [HelperText](../form-field/component.yaml#L19) | Input | Text | <code>="Use a short name your team will recognize."</code> | Instructions shown below the input and included in its accessible label. |
| [Required](../form-field/component.yaml#L25) | Input | Boolean | <code>=true</code> | When true, blank or whitespace-only text is invalid. Errors wait for a changed blur or ShowValidation. |
| [ErrorText](../form-field/component.yaml#L31) | Input | Text | <code>=""</code> | Host-supplied business error. Nonblank text displays immediately and makes IsValid false. The host clears it. |
| [ShowValidation](../form-field/component.yaml#L37) | Input | Boolean | <code>=false</code> | Set true after a host validation attempt to show any required error, including an untouched blank field. |
| [Disabled](../form-field/component.yaml#L43) | Input | Boolean | <code>=false</code> | Disables text editing. This does not clear text, errors, or the Required rule. |
| [Design](../form-field/component.yaml#L49) | Input | Record | [Source formula](../form-field/component.yaml#L49) | Shared design settings. Bind to the complete UiTheme record; the field consumes its text, surface, border, accent, error, and corner values. |
| [Text](../form-field/component.yaml#L85) | Output | Text | — | Current text, updated on each keystroke. Whitespace is preserved. |
| [IsValid](../form-field/component.yaml#L90) | Output | Boolean | — | True when ErrorText is blank and the required rule passes, even before validation is displayed. |
| [OnChange](../form-field/component.yaml#L95) | Event | (NewText: Text) → None | <code>=false</code> | Runs after edited text loses focus. It does not run on each keystroke or an unchanged focus/blur. |

<a id="kanban-board"></a>

## Kanban board

**Studio name:** `lcsKanban` · [Setup guide](../kanban-board/README.md) · [Source](../kanban-board/component.yaml)

| Property | Kind | Type / parameters | Default | Purpose |
| --- | --- | --- | --- | --- |
| [Columns](../kanban-board/component.yaml#L6) | Input | Table | [Source formula](../kanban-board/component.yaml#L6) | The board's columns, left to right: Key, Title and Limit (the most cards the column may hold; 0 for no limit). |
| [Cards](../kanban-board/component.yaml#L18) | Input | Table | [Source formula](../kanban-board/component.yaml#L18) | Every card: Key, Column (the Key of its column), Title, Detail and Tag. Cards show in the order of this table. |
| [CurrentKey](../kanban-board/component.yaml#L33) | Input | Text | <code>=""</code> | The Key of the card to mark as selected, from your app. Leave it blank and the board marks the card last selected. |
| [BlockWhenFull](../kanban-board/component.yaml#L39) | Input | Boolean | <code>=true</code> | When true, a card can't be moved into a column that has reached its Limit: the button to move it there is turned off. |
| [ShowDetail](../kanban-board/component.yaml#L45) | Input | Boolean | <code>=true</code> | Shows each card's Detail line. |
| [ShowTags](../kanban-board/component.yaml#L51) | Input | Boolean | <code>=true</code> | Shows each card's Tag above its title, in your colour. |
| [CardHeight](../kanban-board/component.yaml#L57) | Input | Number | <code>=96</code> | The height of every card, in pixels. Make it taller for long titles. |
| [BoardLabel](../kanban-board/component.yaml#L63) | Input | Text | <code>="Board"</code> | What screen readers call the board. |
| [CardsText](../kanban-board/component.yaml#L69) | Input | Text | <code>="cards"</code> | The word screen readers say after a column's count, such as In progress, 2 cards. |
| [OfText](../kanban-board/component.yaml#L75) | Input | Text | <code>="of"</code> | The word between a column's count and its limit, such as 2 of 3. |
| [FullText](../kanban-board/component.yaml#L81) | Input | Text | <code>="Full"</code> | What a column says when it has reached its limit. |
| [MoveText](../kanban-board/component.yaml#L87) | Input | Text | <code>="Move"</code> | The start of a move button's name, read out and shown on hover, such as Move Fix login to Done. |
| [ToText](../kanban-board/component.yaml#L93) | Input | Text | <code>="to"</code> | The word between the card and the column in a move button's name. |
| [EmptyText](../kanban-board/component.yaml#L99) | Input | Text | <code>="No cards"</code> | What an empty column says. |
| [AccentColor](../kanban-board/component.yaml#L105) | Input | Color | <code>=ColorValue("#463782")</code> | Your brand colour, for tags, the selected card and the focus ring. |
| [Theme](../kanban-board/component.yaml#L111) | Input | Text | <code>="Light"</code> | Light, or Dark for a dark screen. |
| [Motion](../kanban-board/component.yaml#L117) | Input | Boolean | <code>=true</code> | Plays short animations: a card that moves glows, a selected card's outline draws itself, a column that fills up pulses. They never play for people who've asked their device for reduced motion. |
| [SelectedKey](../kanban-board/component.yaml#L123) | Output | Text | — | The Key of the selected card, or blank. |
| [SelectedCard](../kanban-board/component.yaml#L128) | Output | Record | — | The selected card's row from Cards. |
| [CardCount](../kanban-board/component.yaml#L133) | Output | Number | — | How many cards the board has. |
| [FullColumns](../kanban-board/component.yaml#L138) | Output | Text | — | Keys of the columns that have reached their limit, separated by commas. |
| [OnMove](../kanban-board/component.yaml#L143) | Event | (CardKey: Text, ToColumn: Text, FromColumn: Text) → None | <code>=false</code> | Runs when the user moves a card. Change the card's Column in your data here; the board shows it there when Cards changes. |
| [OnCardSelect](../kanban-board/component.yaml#L162) | Event | (CardKey: Text) → None | <code>=false</code> | Runs when the user selects a card. Open its details here. |
| [ClearSelection](../kanban-board/component.yaml#L173) | Action | None | — | Unmarks the selected card, such as after you close its details. |

<a id="kpi-card"></a>

## KPI card

**Studio name:** `lcsKpiCard` · [Setup guide](../kpi-card/README.md) · [Source](../kpi-card/component.yaml)

| Property | Kind | Type / parameters | Default | Purpose |
| --- | --- | --- | --- | --- |
| [Label](../kpi-card/component.yaml#L6) | Input | Text | <code>="Open orders"</code> | What the number is, such as Open orders. |
| [Value](../kpi-card/component.yaml#L12) | Input | Number | <code>=128</code> | The number to show, such as CountIf(Orders, Status = "Open"). |
| [Format](../kpi-card/component.yaml#L18) | Input | Text | <code>="Number"</code> | How to show Value: Number, Currency, Percent (0.42 shows as 42%), or Compact (12,400 shows as 12.4K). |
| [CurrencySymbol](../kpi-card/component.yaml#L24) | Input | Text | <code>="$"</code> | The symbol before a Currency value, such as $ or €. |
| [Decimals](../kpi-card/component.yaml#L30) | Input | Number | <code>=0</code> | How many decimal places to show for Number and Currency. |
| [Previous](../kpi-card/component.yaml#L36) | Input | Number | <code>=112</code> | The value to compare with, such as last week's. Leave it blank to show no change. |
| [ChangeLabel](../kpi-card/component.yaml#L42) | Input | Text | <code>="vs last week"</code> | What the change is against, shown after it, such as vs last week. |
| [GoodWhen](../kpi-card/component.yaml#L48) | Input | Text | <code>="Up"</code> | Up when a rise is good (sales), Down when a fall is good (open tickets), None to colour the change neutrally. |
| [Target](../kpi-card/component.yaml#L54) | Input | Number | <code>=120</code> | A goal to show progress toward as a bar. Leave it blank for no bar. |
| [Status](../kpi-card/component.yaml#L60) | Input | Text | <code>="Auto"</code> | The status that tints the icon's circle and the target bar: Auto (good at or above the target, warning from 70%, bad below), Good, Warning, Bad or Neutral. |
| [Icon](../kpi-card/component.yaml#L66) | Input | Text | <code>="Cart"</code> | A modern icon's name shown in a circle tinted by the status, such as Cart, People or Money. Empty for none. |
| [Caption](../kpi-card/component.yaml#L72) | Input | Text | <code>=""</code> | A small line under the number when there's no change to show, such as Updated 5 min ago. |
| [AccentColor](../kpi-card/component.yaml#L78) | Input | Color | <code>=ColorValue("#463782")</code> | Your brand colour, for the icon, the target bar and the focus ring. |
| [Theme](../kpi-card/component.yaml#L84) | Input | Text | <code>="Light"</code> | Light, or Dark for a dark screen. |
| [Motion](../kpi-card/component.yaml#L90) | Input | Boolean | <code>=true</code> | The target bar fills and the change arrow pops in when the card loads or its values change. None plays for people who've asked their device for reduced motion. |
| [Change](../kpi-card/component.yaml#L96) | Output | Number | — | Value minus Previous; 0 when there's no Previous. |
| [ChangePercent](../kpi-card/component.yaml#L101) | Output | Number | — | The change as a fraction of Previous, such as 0.125 for 12.5%; 0 when there's no Previous or it's 0. |
| [Trend](../kpi-card/component.yaml#L106) | Output | Text | — | Up, Down or Flat. |
| [TargetPercent](../kpi-card/component.yaml#L111) | Output | Number | — | Value as a fraction of Target, capped at 1; 0 when there's no Target. |
| [StatusShown](../kpi-card/component.yaml#L116) | Output | Text | — | The status in effect: Good, Warning, Bad or Neutral, after Auto is worked out. |
| [ValueText](../kpi-card/component.yaml#L121) | Output | Text | — | The number as the card shows it, such as $12.4K, for a tooltip or a summary. |
| [OnSelect](../kpi-card/component.yaml#L126) | Event | None | <code>=false</code> | Runs in your app when the card is selected, such as Navigate to the list behind the number. |

<a id="message-banner"></a>

## Message banner

**Studio name:** `uiMessageBanner` · [Setup guide](../message-banner/README.md) · [Source](../message-banner/component.yaml)

| Property | Kind | Type / parameters | Default | Purpose |
| --- | --- | --- | --- | --- |
| [Title](../message-banner/component.yaml#L7) | Input | Text | <code>="Review the sample project"</code> | Optional short heading. Put the main point first. |
| [Message](../message-banner/component.yaml#L13) | Input | Text | <code>="This page uses fictional data. Review the sample details before continuing."</code> | Required message body. Text wraps and increases ContentHeight. |
| [Intent](../message-banner/component.yaml#L19) | Input | Text | <code>="Info"</code> | Info, Success, Warning, or Error. Unknown and blank values use Info. |
| [ActionLabel](../message-banner/component.yaml#L25) | Input | Text | <code>=""</code> | Optional action label. Blank hides the action. Use a short verb phrase that addresses the message. |
| [Dismissible](../message-banner/component.yaml#L31) | Input | Boolean | <code>=true</code> | Show the Dismiss button. OnDismiss asks the host to hide the instance; it does not resolve the condition. |
| [Design](../message-banner/component.yaml#L37) | Input | Record | [Source formula](../message-banner/component.yaml#L37) | Complete shared UiTheme record. Status colors, surfaces, and corner settings are read from this record. |
| [ContentHeight](../message-banner/component.yaml#L73) | Output | Number | — | Measured content height including padding. Bind the instance Height to Self.ContentHeight. Measurement updates while visible. |
| [OnAction](../message-banner/component.yaml#L78) | Event | None | <code>=false</code> | Run the host action. The host owns validation, resolution, navigation, and changes to this banner's inputs. |
| [OnDismiss](../message-banner/component.yaml#L84) | Event | None | <code>=false</code> | Request dismissal. The host sets this instance's Visible property and restores focus. No condition is resolved automatically. |

<a id="month-calendar"></a>

## Month calendar

**Studio name:** `lcsMonthCalendar` · [Setup guide](../month-calendar/README.md) · [Source](../month-calendar/component.yaml)

| Property | Kind | Type / parameters | Default | Purpose |
| --- | --- | --- | --- | --- |
| [Events](../month-calendar/component.yaml#L6) | Input | Table | [Source formula](../month-calendar/component.yaml#L6) | The events, as a table with Key, Title, Start (a date), End (a date, the same as Start for one day) and Color (a hex, or empty for your accent) columns. |
| [DefaultMonth](../month-calendar/component.yaml#L13) | Input | DateAndTime | <code>=Today()</code> | Any date in the month to show first. The person moves months from there; GoToMonth moves them from your app. |
| [StartOfWeek](../month-calendar/component.yaml#L19) | Input | Text | <code>="Monday"</code> | Monday or Sunday, the first column. |
| [MaxPerDay](../month-calendar/component.yaml#L25) | Input | Number | <code>=3</code> | How many event pills a day shows before +N more. |
| [CellHeight](../month-calendar/component.yaml#L31) | Input | Number | <code>=88</code> | Each day's height. 88 fits three pills; add 20 for each more. |
| [ShowToday](../month-calendar/component.yaml#L37) | Input | Boolean | <code>=true</code> | Shows the Today button in the header. |
| [AccentColor](../month-calendar/component.yaml#L43) | Input | Color | <code>=ColorValue("#463782")</code> | Your brand colour, for today's mark, the selected day, events without a colour and the focus rings. |
| [Theme](../month-calendar/component.yaml#L49) | Input | Text | <code>="Light"</code> | Light, or Dark for a dark screen. |
| [Motion](../month-calendar/component.yaml#L55) | Input | Boolean | <code>=true</code> | The event pills draw in from the left when the month changes, and the selected day's ring pops in. None plays for people who've asked their device for reduced motion. |
| [VisibleMonth](../month-calendar/component.yaml#L61) | Output | DateAndTime | — | The first day of the month on show. |
| [SelectedDate](../month-calendar/component.yaml#L66) | Output | DateAndTime | — | The selected day; blank when none. |
| [EventsInMonth](../month-calendar/component.yaml#L71) | Output | Number | — | How many events touch the month on show. |
| [OnSelectDay](../month-calendar/component.yaml#L76) | Event | (SelectedDate: DateAndTime) → None | <code>=false</code> | Runs in your app when a day is selected, with its date. Open a new-event form here. |
| [OnSelectEvent](../month-calendar/component.yaml#L87) | Event | (Key: Text, Title: Text, Start: DateAndTime) → None | <code>=false</code> | Runs in your app when an event pill is selected, with its key, title and start. |
| [OnMonthChange](../month-calendar/component.yaml#L106) | Event | (Month: DateAndTime) → None | <code>=false</code> | Runs in your app when the month on show changes, with its first day. Load that month's events here. |
| [Next](../month-calendar/component.yaml#L117) | Action | None | — | Shows the next month. |
| [Previous](../month-calendar/component.yaml#L122) | Action | None | — | Shows the month before. |
| [GoToToday](../month-calendar/component.yaml#L127) | Action | None | — | Shows this month and selects today. |
| [GoToMonth](../month-calendar/component.yaml#L132) | Action | (Month: DateAndTime) → None | — | Shows the month of a date. |
| [Select](../month-calendar/component.yaml#L142) | Action | (SelectedDate: DateAndTime) → None | — | Selects a day from your app, moving to its month if needed, without raising OnSelectDay. |

<a id="navigation-shell"></a>

## Navigation shell

**Studio name:** `lcsNavShell` · [Setup guide](../navigation-shell/README.md) · [Source](../navigation-shell/component.yaml)

| Property | Kind | Type / parameters | Default | Purpose |
| --- | --- | --- | --- | --- |
| [Items](../navigation-shell/component.yaml#L6) | Input | Table | [Source formula](../navigation-shell/component.yaml#L6) | The menu, in order: Key (your own id for the item), Label, Icon (a Fluent icon name, such as Home) and Badge (text such as 3, or blank). |
| [Title](../navigation-shell/component.yaml#L19) | Input | Text | <code>="My app"</code> | Your app's name, at the top of the side menu. |
| [CurrentKey](../navigation-shell/component.yaml#L25) | Input | Text | <code>=""</code> | The Key of the screen the user is on, from your app, so the menu marks it. Leave it blank and the menu marks the item last selected. |
| [HiddenKeys](../navigation-shell/component.yaml#L31) | Input | Text | <code>=""</code> | Keys of items to hide, separated by commas, such as for a role. |
| [DisabledKeys](../navigation-shell/component.yaml#L37) | Input | Text | <code>=""</code> | Keys of items to show but not allow, separated by commas. |
| [StartCollapsed](../navigation-shell/component.yaml#L43) | Input | Boolean | <code>=false</code> | Starts the side menu collapsed to its icons. |
| [ScreenWidth](../navigation-shell/component.yaml#L49) | Input | Number | <code>=1366</code> | The width of your screen. Set it to Parent.Width, so the menu becomes a bottom bar on phones. |
| [ScreenHeight](../navigation-shell/component.yaml#L55) | Input | Number | <code>=768</code> | The height of your screen. Set it to Parent.Height. |
| [BottomBarBelow](../navigation-shell/component.yaml#L61) | Input | Number | <code>=640</code> | Below this screen width, the menu is a bottom bar. |
| [MaxBottomItems](../navigation-shell/component.yaml#L67) | Input | Number | <code>=5</code> | How many items the bottom bar shows, from the top of the list. |
| [ExpandedWidth](../navigation-shell/component.yaml#L73) | Input | Number | <code>=240</code> | The width of the side menu when it isn't collapsed. |
| [ShowToggle](../navigation-shell/component.yaml#L79) | Input | Boolean | <code>=true</code> | Shows the button that collapses and expands the side menu. |
| [MenuLabel](../navigation-shell/component.yaml#L85) | Input | Text | <code>="Main menu"</code> | What screen readers call the menu. |
| [CollapseText](../navigation-shell/component.yaml#L91) | Input | Text | <code>="Collapse the menu"</code> | The collapse button's name, read out and shown on hover. |
| [ExpandText](../navigation-shell/component.yaml#L97) | Input | Text | <code>="Expand the menu"</code> | The expand button's name, read out and shown on hover. |
| [ShowUser](../navigation-shell/component.yaml#L103) | Input | Boolean | <code>=true</code> | Shows who is signed in at the bottom of the side menu. |
| [UserName](../navigation-shell/component.yaml#L109) | Input | Text | <code>="Avery Brooks"</code> | The signed-in person's name, such as User().FullName. The avatar shows their initials when there's no picture. |
| [UserDetail](../navigation-shell/component.yaml#L115) | Input | Text | <code>="Admin"</code> | A line under the name, such as their role or User().Email. |
| [UserImage](../navigation-shell/component.yaml#L121) | Input | Image | <code>=""</code> | The person's picture, such as User().Image. Leave it blank for initials. |
| [ShowThemeToggle](../navigation-shell/component.yaml#L127) | Input | Boolean | <code>=true</code> | Shows the sun and moon button that switches between light and dark. |
| [DarkText](../navigation-shell/component.yaml#L133) | Input | Text | <code>="Switch to dark theme"</code> | The theme button's name in light mode, read out and shown on hover. |
| [LightText](../navigation-shell/component.yaml#L139) | Input | Text | <code>="Switch to light theme"</code> | The theme button's name in dark mode. |
| [AccentColor](../navigation-shell/component.yaml#L145) | Input | Color | <code>=ColorValue("#463782")</code> | Your brand colour, for the current item and badges. |
| [Look](../navigation-shell/component.yaml#L151) | Input | Text | <code>="Standard"</code> | Standard, or Premium: a floating card with a soft shadow, your app's mark, a solid pill for the current item and the user in a card. |
| [Theme](../navigation-shell/component.yaml#L157) | Input | Text | <code>="Light"</code> | Light, or Dark for a dark app. The theme button changes it inside the menu; keep your app in step with OnThemeChange. |
| [Motion](../navigation-shell/component.yaml#L163) | Input | Boolean | <code>=true</code> | Plays short animations: the current item's highlight eases in when it changes, and a new badge pulses twice. They never play for people who've asked their device for reduced motion. |
| [IsCollapsed](../navigation-shell/component.yaml#L169) | Output | Boolean | — | True while the side menu is collapsed to its icons. |
| [IsBottomBar](../navigation-shell/component.yaml#L174) | Output | Boolean | — | True while the menu is a bottom bar, on a narrow screen. |
| [SelectedKey](../navigation-shell/component.yaml#L179) | Output | Text | — | The Key of the item the menu marks as current. |
| [CurrentTheme](../navigation-shell/component.yaml#L184) | Output | Text | — | Light or Dark: the Theme input, or what the theme button chose. |
| [ShellX](../navigation-shell/component.yaml#L189) | Output | Number | — | Set the component's X to this. |
| [ShellY](../navigation-shell/component.yaml#L194) | Output | Number | — | Set the component's Y to this. |
| [ShellWidth](../navigation-shell/component.yaml#L199) | Output | Number | — | Set the component's Width to this. |
| [ShellHeight](../navigation-shell/component.yaml#L204) | Output | Number | — | Set the component's Height to this. |
| [ContentX](../navigation-shell/component.yaml#L209) | Output | Number | — | Where your screen's content starts, from the left. |
| [ContentY](../navigation-shell/component.yaml#L214) | Output | Number | — | Where your screen's content starts, from the top. |
| [ContentWidth](../navigation-shell/component.yaml#L219) | Output | Number | — | How wide your screen's content can be. |
| [ContentHeight](../navigation-shell/component.yaml#L224) | Output | Number | — | How tall your screen's content can be. |
| [OnNavigate](../navigation-shell/component.yaml#L229) | Event | (ItemKey: Text) → None | <code>=false</code> | Runs when the user selects an item. Go to its screen here with Navigate, using ItemKey to choose the screen. |
| [OnToggle](../navigation-shell/component.yaml#L240) | Event | (Collapsed: Boolean) → None | <code>=false</code> | Runs when the user collapses or expands the side menu. |
| [OnThemeChange](../navigation-shell/component.yaml#L251) | Event | (NewTheme: Text) → None | <code>=false</code> | Runs when the user switches between light and dark. Set your app's theme here. |
| [OnUserSelect](../navigation-shell/component.yaml#L262) | Event | None | <code>=false</code> | Runs when the user selects their avatar. Open their profile or a sign-out choice here. |
| [SetCollapsed](../navigation-shell/component.yaml#L268) | Action | (Collapsed: Boolean) → None | — | Collapses or expands the side menu, such as SetCollapsed(true) on a small tablet. |

<a id="search-filter-bar"></a>

## Search and filter bar

**Studio name:** `uiSearchFilter` · [Setup guide](../search-filter-bar/README.md) · [Source](../search-filter-bar/component.yaml)

| Property | Kind | Type / parameters | Default | Purpose |
| --- | --- | --- | --- | --- |
| [StatusOptions](../search-filter-bar/component.yaml#L7) | Input | Table | <code>=Table({Value: "Not started"}, {Value: "In progress"}, {Value: "Completed"})</code> | Distinct status choices with one Value text column. An empty All statuses choice is added automatically. |
| [OwnerOptions](../search-filter-bar/component.yaml#L14) | Input | Table | <code>=Table({Value: "Alex"}, {Value: "Jordan"}, {Value: "Morgan"})</code> | Distinct owner choices with one Value text column. An empty All owners choice is added automatically. |
| [SearchPlaceholder](../search-filter-bar/component.yaml#L21) | Input | Text | <code>="Search by title"</code> | Hint for the host app's search rule. The visible label remains Search. |
| [ResultCount](../search-filter-bar/component.yaml#L27) | Input | Number | <code>=-1</code> | The host app's complete filtered result count. A negative number hides the result count. |
| [Disabled](../search-filter-bar/component.yaml#L33) | Input | Boolean | <code>=false</code> | Disables search, both dropdowns, and Clear all without discarding their values. |
| [Design](../search-filter-bar/component.yaml#L39) | Input | Record | [Source formula](../search-filter-bar/component.yaml#L39) | Complete shared UiTheme record. This component reads Accent, Background, Text, TextMuted, ControlBorder, CornerRadius, ButtonShape, and ButtonCornerRadius. |
| [Query](../search-filter-bar/component.yaml#L75) | Output | Text | — | Current search text with leading and trailing spaces removed. Updates on each keystroke. Empty means all titles. |
| [Status](../search-filter-bar/component.yaml#L80) | Output | Text | — | Selected status Value. Empty means all statuses. |
| [Owner](../search-filter-bar/component.yaml#L85) | Output | Text | — | Selected owner Value. Empty means all owners. |
| [ActiveFilterCount](../search-filter-bar/component.yaml#L90) | Output | Number | — | Number of nonempty Query, Status, and Owner values, from zero to three. |
| [OnChange](../search-filter-bar/component.yaml#L95) | Event | None | <code>=false</code> | Runs after edited search text loses focus or a dropdown selection changes. Bind filtering to outputs for live results. |
| [OnClear](../search-filter-bar/component.yaml#L101) | Event | None | <code>=false</code> | Runs after the user selects Clear all. The search and both filters have been reset. |

<a id="stepper"></a>

## Stepper

**Studio name:** `lcsStepper` · [Setup guide](../stepper/README.md) · [Source](../stepper/component.yaml)

| Property | Kind | Type / parameters | Default | Purpose |
| --- | --- | --- | --- | --- |
| [Steps](../stepper/component.yaml#L6) | Input | Table | [Source formula](../stepper/component.yaml#L6) | The steps, in order: Title and Description. |
| [Type](../stepper/component.yaml#L18) | Input | Text | <code>="Steps"</code> | Steps: a form or wizard in your colour. Project: project stages in the standard status colours, finished blue, the current stage green, amber or red for its Health, the rest grey. Approval: an approval chain, approved steps green, the current one amber, red when Health is Red. |
| [Health](../stepper/component.yaml#L24) | Input | Text | <code>="Green"</code> | Project and Approval: the current stage's health. Green (on track), Amber (at risk) or Red (off track; in Approval, rejected). |
| [StatusText](../stepper/component.yaml#L30) | Input | Text | <code>=""</code> | Project and Approval: the words on the status pill. Leave it empty for On track, At risk, Off track or Complete; in Approval, Waiting for approval, Rejected or Approved. |
| [DefaultStep](../stepper/component.yaml#L36) | Input | Number | <code>=1</code> | The step shown when the screen loads, from 1. In Project and Approval, one more than the number of steps shows them all finished. |
| [Orientation](../stepper/component.yaml#L42) | Input | Text | <code>="Horizontal"</code> | Horizontal, or Vertical for a narrow screen or a side panel. |
| [ShowDescriptions](../stepper/component.yaml#L48) | Input | Boolean | <code>=true</code> | Shows each step's Description under its title. |
| [ShowButtons](../stepper/component.yaml#L54) | Input | Boolean | <code>=true</code> | Shows Back and Next. Turn it off to use your own buttons with Back() and Next(). |
| [AllowJumpBack](../stepper/component.yaml#L60) | Input | Boolean | <code>=true</code> | Lets the user select an earlier step to go back to it. |
| [CanLeaveStep](../stepper/component.yaml#L66) | InputFunction | (Step: Number) → Boolean | <code>=true</code> | Your check before the user moves on. Receives the step number and returns true when it's complete. |
| [BackText](../stepper/component.yaml#L77) | Input | Text | <code>="Back"</code> | The Back button's label. |
| [NextText](../stepper/component.yaml#L83) | Input | Text | <code>="Next"</code> | The Next button's label. |
| [FinishText](../stepper/component.yaml#L89) | Input | Text | <code>="Submit"</code> | The Next button's label on the last step. |
| [BlockedText](../stepper/component.yaml#L95) | Input | Text | <code>="Complete this step to continue."</code> | What it says when CanLeaveStep returns false. |
| [StepText](../stepper/component.yaml#L101) | Input | Text | <code>="Step {n} of {total}"</code> | The progress line and each step's name for screen readers. {n} is the step and {total} the count. |
| [DoneText](../stepper/component.yaml#L107) | Input | Text | <code>="completed"</code> | What screen readers add to a finished step. |
| [CurrentText](../stepper/component.yaml#L113) | Input | Text | <code>="current step"</code> | What screen readers add to the step the user is on. |
| [Look](../stepper/component.yaml#L119) | Input | Text | <code>="Standard"</code> | Standard, or Premium: a card with a soft shadow, rounder corners, thicker lines, the current step's title in your colour and a thicker progress bar. |
| [AccentColor](../stepper/component.yaml#L125) | Input | Color | <code>=ColorValue("#463782")</code> | Your brand colour, for finished and current steps and the Next button. |
| [Theme](../stepper/component.yaml#L131) | Input | Text | <code>="Light"</code> | Light, or Dark for a dark screen. |
| [Motion](../stepper/component.yaml#L137) | Input | Boolean | <code>=true</code> | Plays short animations when the step changes: the current step's halo pops and a ring ripples out of it four times, then stays as a solid ring; a step you've just finished draws its check, and the progress bar slides to its new length. All of it ends within five seconds. None plays for people who've asked their device for reduced motion. |
| [CurrentStep](../stepper/component.yaml#L143) | Output | Number | — | The step the user is on, from 1. Show each step's content when this is its number. |
| [StepCount](../stepper/component.yaml#L148) | Output | Number | — | How many steps there are. |
| [CurrentTitle](../stepper/component.yaml#L153) | Output | Text | — | The title of the step the user is on. |
| [IsFirst](../stepper/component.yaml#L158) | Output | Boolean | — | True on the first step. |
| [IsLast](../stepper/component.yaml#L163) | Output | Boolean | — | True on the last step. |
| [Progress](../stepper/component.yaml#L168) | Output | Number | — | How far through, from 0 to 1: the steps finished out of all of them. |
| [Status](../stepper/component.yaml#L173) | Output | Text | — | Project and Approval: the status pill's words, such as At risk. |
| [OnStepChange](../stepper/component.yaml#L178) | Event | (NewStep: Number, OldStep: Number) → None | <code>=false</code> | Runs when the user moves to another step, with Next, Back or an earlier step. |
| [OnFinish](../stepper/component.yaml#L193) | Event | None | <code>=false</code> | Runs when the user selects Next on the last step and CanLeaveStep allows it. Submit here. |
| [GoToStep](../stepper/component.yaml#L199) | Action | (StepNumber: Number) → None | — | Shows a step. Going forward stops at the first step that CanLeaveStep doesn't allow. |
| [Next](../stepper/component.yaml#L209) | Action | None | — | Moves to the next step if CanLeaveStep allows it, as the Next button does (without finishing). |
| [Back](../stepper/component.yaml#L214) | Action | None | — | Moves to the step before. |
| [Reset](../stepper/component.yaml#L219) | Action | None | — | Goes back to DefaultStep and clears the blocked message. |

<a id="tree-view"></a>

## Tree view

**Studio name:** `lcsTreeView` · [Setup guide](../tree-view/README.md) · [Source](../tree-view/component.yaml)

| Property | Kind | Type / parameters | Default | Purpose |
| --- | --- | --- | --- | --- |
| [Nodes](../tree-view/component.yaml#L6) | Input | Table | [Source formula](../tree-view/component.yaml#L6) | Every node as one flat table: Key, ParentKey (blank for the top level), Label, Icon (a Fluent icon name, such as Folder) and HasChildren (true when it has children you load later). |
| [DefaultExpandedKeys](../tree-view/component.yaml#L22) | Input | Text | <code>="docs"</code> | Keys of the nodes open when the screen loads, separated by commas. |
| [CurrentKey](../tree-view/component.yaml#L28) | Input | Text | <code>=""</code> | The Key of the node to mark as selected, from your app. Leave it blank and the tree marks the node last selected. |
| [Title](../tree-view/component.yaml#L34) | Input | Text | <code>="Files"</code> | The heading above the tree. |
| [ShowTitle](../tree-view/component.yaml#L40) | Input | Boolean | <code>=true</code> | Shows the heading. |
| [ShowIcons](../tree-view/component.yaml#L46) | Input | Boolean | <code>=true</code> | Shows each node's icon: folders in amber, everything else in your colour. |
| [ShowCounts](../tree-view/component.yaml#L52) | Input | Boolean | <code>=true</code> | Shows how many children each open or closed folder has, once they're loaded. |
| [ShowGuides](../tree-view/component.yaml#L58) | Input | Boolean | <code>=true</code> | Draws thin lines that join each level to its parent. |
| [Look](../tree-view/component.yaml#L64) | Input | Text | <code>="Standard"</code> | Standard, or Premium: a solid pill in your colour for the selected node and a soft shadow. |
| [IndentSize](../tree-view/component.yaml#L70) | Input | Number | <code>=20</code> | How far each level is indented, in pixels. |
| [TreeLabel](../tree-view/component.yaml#L76) | Input | Text | <code>="Folders"</code> | What screen readers call the tree. |
| [ExpandText](../tree-view/component.yaml#L82) | Input | Text | <code>="Expand"</code> | The start of an open button's name, read out and shown on hover, such as Expand Documents. |
| [CollapseText](../tree-view/component.yaml#L88) | Input | Text | <code>="Collapse"</code> | The start of a close button's name, such as Collapse Documents. |
| [LevelText](../tree-view/component.yaml#L94) | Input | Text | <code>="level"</code> | The word screen readers say before a node's level, such as Plans, level 2. |
| [EmptyText](../tree-view/component.yaml#L100) | Input | Text | <code>="Nothing here yet"</code> | What the tree says when there are no nodes. |
| [AccentColor](../tree-view/component.yaml#L106) | Input | Color | <code>=ColorValue("#463782")</code> | Your brand colour, for the selected node. |
| [Theme](../tree-view/component.yaml#L112) | Input | Text | <code>="Light"</code> | Light, or Dark for a dark screen. |
| [Motion](../tree-view/component.yaml#L118) | Input | Boolean | <code>=true</code> | Plays short animations: a node's highlight eases in when it's selected, and a chevron turns when its folder opens or closes. None plays for people who've asked their device for reduced motion. |
| [SelectedKey](../tree-view/component.yaml#L124) | Output | Text | — | The Key of the selected node, or blank. |
| [SelectedNode](../tree-view/component.yaml#L129) | Output | Record | — | The selected node's row from Nodes. |
| [ExpandedKeys](../tree-view/component.yaml#L134) | Output | Text | — | Keys of the open nodes, separated by commas, to save and pass back as DefaultExpandedKeys. |
| [VisibleCount](../tree-view/component.yaml#L139) | Output | Number | — | How many nodes show now. |
| [OnNodeSelect](../tree-view/component.yaml#L144) | Event | (NodeKey: Text) → None | <code>=false</code> | Runs when the user selects a node. Open what it stands for here. |
| [OnExpand](../tree-view/component.yaml#L155) | Event | (NodeKey: Text) → None | <code>=false</code> | Runs when the user opens a node. Load its children here if you load them as needed. |
| [OnCollapse](../tree-view/component.yaml#L166) | Event | (NodeKey: Text) → None | <code>=false</code> | Runs when the user closes a node. |
| [Expand](../tree-view/component.yaml#L177) | Action | (NodeKey: Text) → None | — | Opens a node, such as Expand(NodeKey) to show where something is. |
| [Collapse](../tree-view/component.yaml#L187) | Action | (NodeKey: Text) → None | — | Closes a node. |
| [ExpandAll](../tree-view/component.yaml#L197) | Action | None | — | Opens every node that has children in Nodes. It doesn't run OnExpand. |
| [CollapseAll](../tree-view/component.yaml#L202) | Action | None | — | Closes every node. |

## Keep this reference current

1. Edit the component source.
2. Run `python scripts/component_reference.py --write`.
3. Run `python scripts/component_reference.py --check`.

Run `python scripts/check_compatibility.py` to check the original public properties. See [preservation findings](COMPONENT-PRESERVATION.md) for the scope and remaining limits.
