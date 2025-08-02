from CodeScribe.comment_generator import generate_comment

def main():
    input_path = "Examples/sample.py"
    output_path = "Examples/sample_commented.py"

    # Read sample code
    with open(input_path, "r") as f:
        code = f.read()

    # Generate commented version of the code
    commented_code = generate_comment(code)

    # Print the result
    print("\n----- Commented Code -----\n")
    print(commented_code)

    # Save to a new file
    with open(output_path, "w") as f:
        f.write(commented_code)

    print(f"\n[✅] Commented code saved to: {output_path}")

if __name__ == "__main__":
    main()
