# GPTs 

This Django project manages GPT (Generative Pre-trained Transformer) instances through a single app called `gpts`. It provides APIs to interact with GPT models, allowing users to view, upvote, and add new models.

## Installation

1. Clone the repository:

```bash
git clone <repository_url>
cd <project_directory>
```

2. Install the required Python packages:

```bash
pip install -r requirements.txt
```

3. Run database migrations:

```bash
python manage.py migrate
```

4. Start the development server:

```bash
python manage.py runserver
```

## Usage

### Models

The `gpts` app defines the following models:

- **Owner**: Represents the owner of a GPT instance.
- **Tags**: Represents tags associated with GPT instances.
- **TimeSeriesPoint**: Stores time-series data for upvotes and views.
- **ActivitySummary**: Represents the activity summary of a GPT instance.
- **GPT**: Represents a GPT instance with its associated metadata and activity summary.

### Views

The following views are available in the `gpts` app:

- **get_models**: Retrieves all GPT instances with their metadata.
- **get_model_details**: Retrieves details of a specific GPT instance.
- **update_upvote**: Increments the upvote count for a GPT instance.
- **update_view**: Increments the view count for a GPT instance.
- **add_gpt_model**: Adds a new GPT instance.
- **get_all_tags**: Retrieves all available tags.
- **get_all_owners**: Retrieves all owners.

### URLs

The API endpoints for the `gpts` app are configured as follows:

- `/api/model`: GET (get_models), POST (add_gpt_model)
- `/api/model/<id>`: GET (get_model_details), POST (update_upvote, update_view)
- `/api/model/<id>/upvote`: POST (update_upvote)
- `/api/model/<id>/view`: POST (update_view)
- `/api/tags`: GET (get_all_tags)
- `/api/owners`: GET (get_all_owners)

## Contributors

- [Manish Singh](https://github.com/astromanish)
