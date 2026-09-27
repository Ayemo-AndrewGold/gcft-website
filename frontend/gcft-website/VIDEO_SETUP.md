# Video Setup Instructions

## Current Status

✅ **Video component is working!** The hero section is currently using a test video from Google's sample library.

## Test Video

The site is currently using this test video:
```
https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4
```

You should see this video playing in the background when you run `npm run dev` and visit the site.

## Adding Your Own Video

### Step 1: Prepare Your Video File

1. **Format**: MP4 with H.264 codec
2. **Resolution**: 1920x1080 (1080p) or 1280x720 (720p)
3. **Duration**: 10-30 seconds for a good loop
4. **File size**: Under 5MB for web performance
5. **Audio**: Remove audio track (video will be muted anyway)

### Step 2: Add Files to Public Directory

Place these files in `/public/`:
- `hero-video.mp4` - Your main video file
- `hero-poster.jpg` - A poster image (same aspect ratio as video)

### Step 3: Update the Code

In `src/app/page.tsx`, change:

```tsx
// FROM:
<HeroSection 
  videoSrc="https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4" 
  posterSrc="/hero-poster.svg"
/>

// TO:
<HeroSection 
  videoSrc="/hero-video.mp4" 
  posterSrc="/hero-poster.jpg"
/>
```

### Recommended Video Content for Church/Ministry

- Worship service moments
- Church building exterior/interior shots
- People in worship, prayer, or fellowship
- Pastor teaching or preaching (b-roll footage)
- Cross, stained glass, or other Christian symbols
- Community gathering moments
- Scenic shots with spiritual atmosphere

### Free Video Resources

- **Pexels.com**: Search "church", "worship", "prayer", "cross"
- **Pixabay.com**: High-quality free videos
- **Unsplash.com**: For poster images
- **Coverr.co**: Short looping videos perfect for backgrounds

### Video Compression Tips

Use tools like:
- **HandBrake** (free): Compress video while maintaining quality
- **FFmpeg**: Command-line tool for video processing
- **Adobe Media Encoder**: Professional compression
- **Online tools**: CloudConvert, etc.

Example FFmpeg command:
```bash
ffmpeg -i input.mp4 -c:v libx264 -crf 28 -c:a aac -b:a 128k -movflags +faststart output.mp4
```

### Testing Video Playback

1. Run `npm run dev`
2. Open browser to `http://localhost:3000`
3. Check browser console for any video errors
4. Test on mobile devices (some browsers have stricter autoplay policies)

### Troubleshooting

**Video won't play:**
- Check file format (MP4 with H.264)
- Ensure file path is correct
- Check browser console for errors
- Try a different browser
- Mobile browsers may require user interaction to play

**Video is too large:**
- Compress the video file
- Consider using a shorter loop
- Reduce resolution if necessary

**Video doesn't loop smoothly:**
- Ensure first and last frames are similar
- Use video editing software to create seamless loops

## Current Features Working

✅ Autoplay (muted)  
✅ Loop  
✅ Responsive scaling  
✅ Dark overlay for text readability  
✅ Reduced motion support  
✅ Poster image fallback  
✅ Cross-browser compatibility  

The video background is fully functional - just add your own video file to personalize it!