@router.post("/api/products/upload_pdf")
async def upload_pdf(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        # Read the PDF file using MuPDF
        pdf_document = fitz.open(stream=await file.read(), filetype="pdf")
        pdf_text = ""
        for page in pdf_document:
            pdf_text += page.get_text()

        # Print the extracted text from the PDF
        # print("pdf_text:", pdf_text)

        # Prepare the input text for the language model
        messages = [
            (
                "system",
                "You are a translator. Only return this data in JSON format: {"
                '"name": "string", '
                '"description": "string", '
                '"price": 0, '
                '"currency": "string", '
                '"brand": "string", '
                '"category": "string", '
                '"stock_quantity": 0, '
                '"average_rating": 0, '
                '"total_reviews": 0, '
                '"specifications": {'
                '"additionalProp1": "string", '
                '"additionalProp2": "string", '
                '"additionalProp3": "string"'
                "}"
                "}"
            ),
            (
                "human",
                f"Here is the text, translate it into English if it is not in English and then just provide the JSON for the text and remove all \n and also remove any irrelveant data just give me the JSON file: {pdf_text}"
            )
        ]

        # Invoke the language model
        ai_msg = llm.invoke(messages)
        
        name=llm.invoke(f"just give me the name of the product name{ai_msg}")
        description=llm.invoke(f"just give me the name of the product description{ai_msg}")
        
    
        # json_start = content.find('{')
        # json_end = content.rfind('}') + 1
        # json_content = content[json_start:json_end]
        
        # Parse the JSON content
        # try:
        #     product_data = json.loads(json_content)
        #     print("Extracted JSON data:", json.dumps(product_data, indent=4))
        # except json.JSONDecodeError as e:
        #     print("Failed to decode JSON:", str(e))

        # Generate embedding for the product
        # return({"dfdf": "asdasd"})
        texter = name + " " + description
        product_embedding = embeddings_model.embed_query(texter)

        # Connect to the PostgreSQL database
        conn = psycopg2.connect(**db_connection)
        cur = conn.cursor()
        product_data=""

        try:
            # Insert product data into the database
            cur.execute("""
                INSERT INTO products (
                    name, description, price, currency, brand, category, stock_quantity, average_rating, total_reviews,
                    specifications, created_at, updated_at, embedding
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id, name, description, price, currency, brand, category, stock_quantity, average_rating, total_reviews,
                specifications, created_at, updated_at, embedding
            """, (
                name, description, 3, "USD", product_data["brand"],
                product_data["category"], product_data["stock_quantity"], product_data["average_rating"], product_data["total_reviews"],
                product_data["specifications"], datetime.datetime.utcnow(), datetime.datetime.utcnow(), product_embedding
            ))

            # Fetch the inserted product to return as a response
            inserted_product = cur.fetchone()

            if not inserted_product:
                raise HTTPException(status_code=404, detail="Product not found after insertion")

            # Commit the transaction
            conn.commit()

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

        # Return the AI response
        return {"ai": ai_msg}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))