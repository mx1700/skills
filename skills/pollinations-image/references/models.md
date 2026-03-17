# Pollinations Image Models

## Available Image Models

| Model | Description | Best For | Quality | Speed |
|-------|-------------|----------|---------|-------|
| `zimage` | Default model, good balance of quality and speed | General purpose, everyday images | Good | Medium |
| `flux` | High-quality flux model | High quality images, professional work | Excellent | Slow |
| `turbo` | Fast generation | Quick previews, testing ideas | Basic | Fast |
| `gptimage` | GPT-based image generation | Complex compositions, detailed scenes | Very Good | Medium |
| `seedream` | Seedream model | Artistic styles, creative works | Good | Medium |
| `nanobanana` | Creative model | Experimental, unique styles | Variable | Medium |
| `nanobanana-pro` | Pro version of nanobanana | Professional, commercial work | Excellent | Slow |

## Model Selection Guidelines

### When to use each model:

1. **zimage** (Recommended default)
   - General image generation
   - When unsure which model to use
   - Balanced quality and speed

2. **flux**
   - High-quality professional images
   - When user asks for "高清", "高质量", "professional"
   - Landscape, portrait, detailed scenes

3. **turbo**
   - Quick previews and tests
   - When user wants fast results
   - Idea exploration

4. **gptimage**
   - Complex scenes with multiple elements
   - Detailed descriptions
   - When prompt is very specific

5. **seedream**
   - Artistic and creative styles
   - Paintings, illustrations
   - When user mentions "艺术风格", "绘画风格"

6. **nanobanana / nanobanana-pro**
   - Experimental and unique outputs
   - Creative projects
   - When user wants something different

## Size Recommendations

| Use Case | Width | Height | Aspect Ratio |
|----------|-------|--------|--------------|
| Default | 1024 | 768 | 4:3 |
| HD/Large | 1600 | 1200 | 4:3 |
| Square | 1024 | 1024 | 1:1 |
| Portrait | 768 | 1024 | 3:4 |
| Wide | 1600 | 900 | 16:9 |
| Ultra Wide | 1920 | 1080 | 16:9 |

## Prompt Engineering Tips

1. **Be specific**: Include details about colors, lighting, style
2. **Use adjectives**: "beautiful", "dramatic", "serene", "vibrant"
3. **Specify style**: "photorealistic", "painting", "cartoon", "minimalist"
4. **Include composition**: "close-up", "wide shot", "from above"
5. **Add mood**: "peaceful", "energetic", "mysterious"

## Common Use Cases

### Landscape
- Use: `flux` or `zimage`
- Size: 1600×1200 or 1920×1080
- Prompt tips: Include time of day, weather, season

### Portrait
- Use: `flux` or `gptimage`
- Size: 768×1024
- Prompt tips: Include facial features, expression, clothing

### Logo/Design
- Use: `nanobanana` or `seedream`
- Size: 1024×1024
- Prompt tips: Specify style, colors, simplicity

### Product
- Use: `flux` or `zimage`
- Size: 1024×1024
- Prompt tips: Include background, lighting, perspective
