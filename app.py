from flask import Flask, render_template, request
import wikipedia

app = Flask(__name__)

# Set the language for Wikipedia pages
wikipedia.set_lang('en')

@app.route('/', methods=['GET', 'POST'])
def index():
    summary = ''
    page_image = ''
    if request.method == 'POST':
        page_title = request.form['page_title']
        try:
            # Fetch a detailed summary (first 5 sentences)
            summary = wikipedia.summary(page_title, sentences=5)
            
            # Get the page object to extract images
            page = wikipedia.page(page_title)
            
            # If images are available, use the first one; otherwise, use a placeholder image
            if page.images and len(page.images) > 0:
                page_image = page.images[0]
            else:
                page_image = 'https://via.placeholder.com/300'
        except wikipedia.exceptions.DisambiguationError as e:
            options = ", ".join(e.options[:5])
            summary = f"The search term is ambiguous, please be more specific. Options: {options}"
            page_image = 'https://via.placeholder.com/300'
        except wikipedia.exceptions.PageError:
            summary = "Page not found, please try a different search term."
            page_image = 'https://via.placeholder.com/300'
        except Exception as e:
            summary = f"An error occurred: {str(e)}"
            page_image = 'https://via.placeholder.com/300'

    return render_template('index.html', summary=summary, image=page_image)

if __name__ == '__main__':
    app.run(debug=True)
